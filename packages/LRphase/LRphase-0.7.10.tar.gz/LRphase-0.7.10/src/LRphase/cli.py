# coding=utf-8

import sys, os, re
from argparse import ArgumentParser, Namespace, _ArgumentGroup, _SubParsersAction
from LRphase.SimulatePhasedData import *
from LRphase.InputData import *
from LRphase import urls
from pysam import AlignmentFile, VariantFile
import numpy as np
#from plfit import plfit
import powerlaw
import time
from LRphase.PhaseSet import powlaw_modified, _estimate_prior_probabilities

__version__ = "0.7.10"

def phasing(args):
    """Main function for phasing mode

    Args:
        args:
    """
    sys.stderr.write('\nAnalyzing inputs using phasing mode...\n\n')
    #sys.stderr.write("%s\n" % args)
    # Input data initialization currently ignores much of the content of args. May be a good idea to fix this.
    # TO-DO: Need to actually handle VCF samples properly instead of relying on args.one_sample.
    input_data = InputData(args.output_directory_name,
                           sample = args.one_sample,
                           ignore_samples = args.ignore_samples,
                           reference_sequence_input = args.reference_genome,
                           reference_sequence_input_assembly = args.reference_assembly,
                           max_threads = args.threads,
                           quiet = args.quiet_mode,
                           silent = args.silent_mode
    )
    input_data.add_haplotype_information(args.vcf_file_name)
    input_data.add_reference_sequence(args.reference_genome,
                                      reference_sequence_input_assembly = args.reference_assembly,
                                      output_directory = args.output_directory_name)
    try:
        input_data.add_reads(args.long_read_inputs, sample = args.one_sample, quiet = args.quiet_mode, silent = args.silent_mode)
    except OSError as e:
        sys.stderr.write("%s\n" % e())
        exit(2)
    sys.stderr.write("Phasing reads...\n")
    i=0
    for phasable_sample in input_data:
        sys.stderr.write('Processing alignments for sample %d (%s)...\n' % (i, phasable_sample.sample))
        header_template_file = AlignmentFile(phasable_sample.alignment_file_paths[i], 'rb')

        # Instantiate output file(s)
        if args.output_mode == 'combined':
            combined_output_bam = AlignmentFile('%s/%s.combined_phasing_results.bam' % (args.output_directory_name, phasable_sample.sample),
                                                'wb', template = header_template_file)
        else:
            unphased_output_bam = AlignmentFile('%s/%s.unphased.bam' %  (args.output_directory_name, phasable_sample.sample),
                                                'wb', template = header_template_file)
            nonphasable_output_bam = AlignmentFile('%s/%s.nonphasable.bam' %  (args.output_directory_name, phasable_sample.sample),
                                                   'wb', template = header_template_file)
            if args.output_mode == 'phase_tagged':
                phased_output_bam = AlignmentFile('%s/%s.phase_tagged.bam' %  (args.output_directory_name, phasable_sample.sample),
                                                  'wb', template = header_template_file)
            elif args.output_mode == 'full':
                maternal_output_bam = AlignmentFile('%s/%s.maternal.bam' %  (args.output_directory_name, phasable_sample.sample),
                                                    'wb', template = header_template_file)
                paternal_output_bam = AlignmentFile('%s/%s.paternal.bam' %  (args.output_directory_name, phasable_sample.sample),
                                                    'wb', template = header_template_file)
                
        # Phase reads and write output to approriate file(s)
        for alignment in phasable_sample:
            phased_read = PhasedRead(alignment,
                                     vcf_file = phasable_sample.vcf_file_path,
                                     sample = phasable_sample.sample,
                                     powlaw_alpha = args.powlaw_alpha,
                                     powlaw_xmin = args.powlaw_xmin
            )

            # Make sure reads are tagged appropriately, according to output options.
            if args.add_phasing_tag_to_output:
                # Tag with estimated error rate based on fitted power-law model.
                phased_read.aligned_segment.set_tag(tag = 'ER', value = str(phased_read.phasing_error_rate), value_type='Z', replace=True)
                if phased_read.is_phased:
                    if (args.log_likelihood_threshold > 0 and phased_read.log_likelihood_ratio >= args.log_likelihood_threshold) or phased_read.phasing_error_rate <= args.error_rate_threshold:
                        # Phased read passing the error rate/score threshold.
                        pass
                    else:
                        # Phasing score does not pass threshold. Label as unphased.
                        phased_read.aligned_segment.set_tag(tag = 'HP', value = "unphased", value_type='Z', replace=True)
                elif phased_read.is_Unphased:
                    phased_read.aligned_segment.set_tag(tag = 'HP', value = "unphased", value_type='Z', replace=True)
                else: # Nonphasable
                    phased_read.aligned_segment.set_tag(tag = 'HP', value = "nonphasable", value_type='Z', replace=True)
                    
            # Write output to appropriate destination file(s)
            if args.output_mode == 'combined':
                write_combined_bam_output(phased_read, combined_output_bam, args)
            elif args.output_mode == 'phase_tagged':
                write_phase_tagged_bam_output(phased_read, phased_output_bam, unphased_output_bam,
                                              nonphasable_output_bam, args)
            elif args.output_mode == 'full':
                write_full_bam_output(phased_read, maternal_output_bam, paternal_output_bam,
                                      unphased_output_bam, nonphasable_output_bam, args)                
            
        # Close output file(s)(
        for outfile in ["combined_output_bam", "unphased_output_bam", "nonphasable_output_bam",
                        "phased_output_bam", "maternal_output_bam", "paternal_output_bam"]:
            if outfile in locals():
                locals()[outfile].close()
                
        i += 1
        
    return


def write_combined_bam_output(phased_read, combined_output_bam, args):
    """
    Write phased, unphased, and nonphasable reads to a single output file.
    """
    phased_read.write_to_bam(output_bam_pysam = combined_output_bam)
    return


def write_phase_tagged_bam_output(phased_read, phased_output_bam,
                                  unphased_output_bam, nonphasable_output_bam, args):
    """
    Write phased reads to a single output file, with unphased and nonphasable
    reads written to their own files.

    """
    if phased_read.is_phased:
        if (args.log_likelihood_threshold > 0 and phased_read.log_likelihood_ratio >= args.log_likelihood_threshold) or phased_read.phasing_error_rate <= args.error_rate_threshold:
            # Phased read passing the error-rate/score threshold.
            phased_read.write_to_bam(output_bam_pysam = phased_output_bam)
        else:
            # Phasing score does not pass threshold. Treat as unphased.
            phased_read.write_to_bam(output_bam_pysam = unphased_output_bam)
    elif phased_read.is_Unphased:
        phased_read.write_to_bam(output_bam_pysam = unphased_output_bam)
    else: # Nonphasable
        phased_read.write_to_bam(output_bam_pysam = nonphasable_output_bam)
    return
            

def write_full_bam_output(phased_read, maternal_output_bam, paternal_output_bam,
                          unphased_output_bam, nonphasable_output_bam, args):
    """
    Write maternal and paternal phased reads to separate output files, with 
    unphased and nonphasable reads written to their own files.
    """
    # TO-DO: Need to handle all possible levels of ploidy.
    if phased_read.is_phased:
        if (args.log_likelihood_threshold > 0 and phased_read.log_likelihood_ratio >= args.log_likelihood_threshold) or phased_read.phasing_error_rate <= args.error_rate_threshold:
            if phased_read.phase == 1:
                phased_read.write_to_bam(output_bam_pysam = paternal_output_bam)
            else:
                phased_read.write_to_bam(output_bam_pysam = maternal_output_bam)
        else:
            # Phasing score does not pass threshold. Label as unphased and handle accordingly.
            phased_read.write_to_bam(output_bam_pysam = unphased_output_bam)
    elif phased_read.is_Unphased:
        phased_read.write_to_bam(output_bam_pysam = unphased_output_bam)
    else: # Nonphasable
        phased_read.write_to_bam(output_bam_pysam = nonphasable_output_bam)
    return



def phasability(args):
    """Main function for phasability mode

    Args:
        args:
    """
    
    print('phasability mode')
    #print(args)

    # First precompute error rates over a (un)reasonable range of heterozygous site counts.
    max_hets = 1000
    prior_probs = _estimate_prior_probabilities()
    _error_rate_table = _calculate_error_rate_table(max_hets, args.sequencing_error_rate,
                                                    prior_probs, args.powlaw_alpha, args.powlaw_xmin)

    # Load up the variants
    vcf_file = VariantFile(args.vcf_file_name)

    # Load up chrom_sizes/intervals
    if args.regions:
        intervals = _build_intervals_from_bed_file(args.regions)
    else:
        intervals = _build_intervals_from_chrom_sizes_dict(_chrom_sizes_dict_from_file(args.chrom_sizes))

    # Step through windows, pulling out variant counts and
    # returning the associated error rates.
    with open("%s/estimated_phasability.wig" % args.output_directory_name, 'w') as outfile:
        # Print the wiggle file header
        outfile.write('track type=wig name="Phasability" description="Phasability Plot"\n')
        for interval in intervals:
            chrom, int_start, int_end = interval

            # Make sure chromosome is in VCF
            if chrom not in list(vcf_file.header.contigs):
                continue
            
            # Print wig header
            outfile.write("fixedStep chrom=%s start=%s step=%d span=%d\n" % (chrom, int_start, args.step_size, args.step_size))

            # Step through windows within the chromosome
            win_start = int_start
            win_end = win_start + args.window_size
            while win_start < win_end and win_end <= int_end:
                n_hets = len([het for het in vcf_file.fetch(chrom, win_start, win_end)])
                if n_hets > max_hets:
                    # Have to calculate if more hets than anticipated
                    error_rate = _calculate_error_rate_from_het_count(n_hets, args.sequencing_error_rate,
                                                                      prior_probs,
                                                                      args.powlaw_alpha, args.powlaw_xmin)
                else:
                    # Use precomputed values
                    error_rate = _error_rate_table[n_hets]
                outfile.write("%.5f\n" % (1-error_rate))

                win_start += args.step_size
                win_end = win_start + args.window_size
                if win_end > int_end:
                    win_end = int_end
            
    # Clean up after ourselves
    vcf_file.close()    
    
    return


def _build_intervals_from_bed_file(bed_file):
    """
    Build a list of intervals (simply tuples of chrom, start, end) from
    a BED file.
    """
    ret = []
    with open(bed_file, 'r') as infile:
        for line in infile:
            if re.match('^#', line):  # Comment line
                continue
            rec = line.strip('\n').split()
            ret.append((rec[0], rec[1], rec[2]))
    return ret


def _build_intervals_from_chrom_sizes_dict(chrom_sizes):
    """
    Build a list of intervals from the chrom_sizes dict.
    """
    ret = []
    for chrom in chrom_sizes.keys():
        ret.append((chrom, 1, chrom_sizes[chrom]))
    return ret


def _chrom_sizes_dict_from_file(chrom_sizes):
    """
    Load chrom_sizes entries from a file into a dictionary.
    """
    chrom_sizes_dict = {}
    with open(chrom_sizes, 'r') as chrom_sizes_file:
        for line in chrom_sizes_file:
            rec = line.strip('\n').split()
            chrom_sizes_dict[rec[0]] = int(rec[1])
    return(chrom_sizes_dict)
    

def _calculate_error_rate_from_het_count(het_count, sequencing_error_rate, prior_probs, powlaw_alpha, powlaw_xmin):
    """
    Caclulate an empirical error rate given a discrete het count, sequencing
    error rate, bayesian priors, and powlaw alpha and xmin.
    """
    if het_count <= powlaw_xmin:
        return 1
    x = (het_count  * np.log10(1 - sequencing_error_rate)) + max(prior_probs)
    y = (het_count * np.log10(sequencing_error_rate/3)) + min(prior_probs)
    # We need a heuristic to handle the fact that values below xmin return non-probabilities.
    e = min(1, powlaw_modified(x-y, powlaw_alpha, powlaw_xmin))
    return(e)


def _calculate_error_rate_table(max_hets, sequencing_error_rate, prior_probs, powlaw_alpha, powlaw_xmin):
    """
    Precompute empirical phasing error rates across a range of heterozygous count sites.
    Returns a list of error rates for heterozygous site counts from 0 to max_hets. These
    represent the error rates expected given a perfect match to a single phase, given a
    power law distribution with parameters powlaw_alpha and powlaw_xmin.
    """
    # This calculation is only correct for the diploid case!!

    # Numerator (all positions match)
    # For ploidy > 2, we would need to pick a specific phase and use the correct prior.
    x = np.array(range(1,max_hets+1))
    x = (x * np.log10(1 - sequencing_error_rate)) + max(prior_probs)
    
    # Denominator (all positions mismatch)
    # For ploidy > 2, this would need to be a loop over all other alleles,
    # with appropriate attention paid to using the correct prior for each.
    y = np.array(range(1,max_hets+1))
    y = (y * np.log10(sequencing_error_rate/3)) + min(prior_probs)

    # Convert to log-odds-ratios
    r = x - y

    # Extract error rates
    ret = []
    for i in range(max_hets):
        # We need a heuristic to handle the fact that values below xmin return non-probabilities.
        e = min(1, powlaw_modified(r[i], powlaw_alpha, powlaw_xmin))
        ret.append(e)
    # Handle zero case
    ret.insert(0,1)
    return(ret)

def error_analysis(args):
    """Main simulation mode

    Args:
        args:
    """    
    start_time = time.time()
    sys.stderr.write('\nPerforming error analysis using simulation mode...\n')
    sys.stderr.write('Analysis started %s.\n\n' % time.asctime())
    input_data = InputData(args.output_directory_path,
                           sample = args.one_sample,
                           ignore_samples = args.ignore_samples,
                           reference_sequence_input = args.reference_genome,
                           reference_sequence_input_assembly = args.reference_assembly,
                           max_threads = args.threads,
                           quiet = args.quiet_mode,
                           silent = args.silent_mode
    )
    input_data.add_haplotype_information(args.vcf_file_path)
    input_data.add_reference_sequence(args.reference_genome,
                                      reference_sequence_input_assembly = args.reference_assembly,
                                      output_directory = args.output_directory_path)

    if args.autosomal_only:
        # Only do simulations for autosomal sequences
        autosomal_ref_seq_path = create_fasta_file(
            input_fasta_file_path = args.reference_genome,
            output_fasta_file_path =  args.output_directory_path + '/reference_sequences/autosomal_' + args.reference_assembly + '_ref.fa',
            only_autosomal= True,
            chrom_sizes = args.chrom_sizes
        )
    else:
        autosomal_ref_seq_path = args.reference_genome
    
    """
    Some of what is implemented below is already contained in SimulatePhasedData.py and
    PhaseSet.py. However, I am choosing to reimplement here because I feel it will be faster
    and more efficient from a development standpoint to do so than to try and parse out how
    to use the object methods that Greg implemented. This should probably be addressed in
    a future release. --AGD
    """
    
    # Prepare the haploytpe-specific fasta
    haplotypes = [1,2]  # TO-DO: Extract the number of haplotypes from the VCF
    haplotype_specific_fasta = []
    chain_file_paths = []
    for haplotype in haplotypes:
        hsf, cfp = generate_haplotype_specific_fasta(
            haplotype,
            args.one_sample,
            autosomal_ref_seq_path,
            args.vcf_file_path,
            output_reference_sequence_path =
            args.output_directory_path +
            '/reference_sequences/autosomal_' +
            args.reference_assembly +
            '_ref_' +
            args.one_sample +
            '_hap' + str(haplotype) + '.fa',
            chain_file_path =
            args.output_directory_path +
            '/reference_sequences/autosomal_' +
            args.reference_assembly +
            '_ref_' +
            args.one_sample  +
            '_hap' + str(haplotype) + '.chain'
        )
        haplotype_specific_fasta.append(hsf)
        chain_file_paths.append(cfp)

    # Simulate reads at 1X depth for N iterations to achieve the necessary number of total reads.
    # Each 1X simulation is expected to produce ~ 190k reads.
    # TO-DO: - Simulate over all samples in VCF.
    #        - Make function args configurable through command-line options.
    #        - Add option to iterate until a minimum number of error observations
    #          are collected.
    hist_all = np.array([])
    hist_err = np.array([])
    bins = np.array([])
    error_lr_list = []
    error_read_list = []

    # Kludge to avoid needing a separate loop when args.simulation_min_err_obs is set:
    if args.simulation_min_err_obs > 0:
        args.simulation_depth = 9999999999999  # We just need an unreasonably large number of iterations to be safe!

    # Open a file for per-iteration simulation stats, if requested
    if args.store_simulation_data_for_iterations:
        per_iteration_stats_file = open(args.output_directory_path + "/per_iteration_simulation_error_stats.tsv", "w")
        
    sys.stderr.write("\n################ Simulating Error Data ################\n")
    for i in range(args.simulation_depth):
        sys.stderr.write("Starting iteration %d...\n" % (i+1))
        total_err_obs = len(error_lr_list)
        
        hist_all_i, hist_err_i, bins_i, error_lr_list_i, error_read_list_i = simulate_results_for_iteration(
            input_data,
            haplotypes,
            haplotype_specific_fasta,
            args
        )
        for j in range(len(error_lr_list_i)):
            error_lr_list.append(error_lr_list_i[j])
            error_read_list.append(error_read_list_i[j])
            
        if i > 0:
            # Combine with results of earlier iterations
            hist_all, hist_err, bins = combine_hists_and_bins(hist_all, hist_all_i,
                                                              hist_err, hist_err_i,
                                                              bins, bins_i,
                                                              args.log_likelihood_ratio_interval
            )
        else:
            hist_all, hist_err, bins = (hist_all_i, hist_err_i, bins_i)

        err_obs_i = len(error_lr_list) - total_err_obs
        sys.stderr.write("Iteration %d produced %d error observations.\n" % (i+1, err_obs_i))

        # Write cumulative error stats for each iteration to disk if requested
        if args.store_simulation_data_for_iterations:
            write_simulation_stats_for_iteration(hist_all, hist_err, bins, i, err_obs_i, len(error_lr_list), per_iteration_stats_file)
            
        # The rest of the kludge for using args.simulation_min_err_obs to control simulations:
        if args.simulation_min_err_obs > 0 and len(error_lr_list) >= args.simulation_min_err_obs:
            break

    # Close the per-iteration stats file if necessary.
    if args.store_simulation_data_for_iterations:
        close(per_iteration_stats_file)

    sys.stderr.write("\n################ Fitting Error Model ################\n")
    with open(args.output_directory_path + "/simulation_error_stats.tsv", "w") as outfile:
        outfile.write("log-odds-bin\ttotal-phased\ttotal-incorrect\teffective-error-rate\n")
        for i in range(len(hist_all)):
            err_rate = -1
            if hist_all[i] > 0:
                err_rate = hist_err[i]/hist_all[i]
            outfile.write("%.5f\t%d\t%d\t%.5f\n" % (bins[i], hist_all[i], hist_err[i], err_rate))
    # Fit the power-law model based on the observed log-likelihood-ratios and associated error rates.
    pl_fit = powerlaw.Fit(error_lr_list, method="KS")

    # Apply a linear xmin correction based on sample-size. 3.585 is the intercept term derived
    # from fitting a linear model to the difference between actual and estimated xmin values
    # over many sets of values sampled from powerlaw distributions with known parameters. We have
    # shown this correction to reduce the bias in xmin estimates across a wide range of sample sizes.
    corrected_xmin = ( pl_fit.xmin * (3.585 / np.log(len(error_lr_list))) ) + 3
    
    with open(args.output_directory_path + "/simulation_error_model_output.txt", 'w') as outfile:
        outfile.write("Total errors in simulations: %d\nMin log-likelihood-ratio for errors: %.3f\nMax log-likelihood ratio for errors: %.3f\nPowerlaw fitting method: %s\nNumber of observations used in powerlaw fitting: %d\nFitted powerlaw alpha: %.5f\nFitted powerlaw xmin: %.5f\nCorrected powerlaw xmin: %.5f\nFitted powerlaw minimum xmin distance (D): %.3f\nFitted powerlaw sigma: %.5f\n" % (len(error_lr_list), min(error_lr_list), max(error_lr_list), pl_fit.fit_method, pl_fit.n, pl_fit.alpha, pl_fit.xmin, corrected_xmin, pl_fit.D, pl_fit.sigma) )

    # Write the full error_lr_list to a file, if requested.
    if args.store_error_probs:
        with open(args.output_directory_path + "/error_lr_list.txt", 'w') as outfile:
            outfile.write("%s\n" % ",".join(error_lr_list))

    # Write detailed information on simulated error reads, if requested.
    if args.save_read_stats:        
        with open(args.output_directory_path + "/error_read_stats.txt", 'w') as outfile:
            outfile.write("seq_name\tlength\tseq_error_rate_avg\tn_hets\tphase\tn_matches_to_phase\tn_mismatches_to_phase\tlog_likelihood_hap1\tlog_likelihood_hap2\tlog_likelihood_ratio\tphasing_err_rate\n")
            for err_read in error_read_list:
                outfile.write("%s\t%d\t%.5f\t%d\t%d\t%d\t%d\t%.5f\t%.5f\t%.5f\t%.5f\n" % (
                    err_read.read_name,
                    err_read.aligned_segment.reference_length,
                    np.mean(err_read.PhaseSet_max.read_base_error_rates),
                    err_read.PhaseSet_max.total_hets_analyzed,
                    err_read.phase,
                    err_read.PhaseSet_max.matches,
                    err_read.PhaseSet_max.non_matches,
                    err_read.PhaseSet_max.log_probability_read_given_haplotype_i[0],
                    err_read.PhaseSet_max.log_probability_read_given_haplotype_i[1],
                    err_read.log_likelihood_ratio,
                    err_read.phasing_error_rate
                    )
                )

    runtime = time.time() - start_time
    sys.stderr.write('Analysis finished %s.\nTotal runtime %.2f seconds.\n' % (time.asctime(), runtime))
    return


def write_simulation_stats_for_iteration(hist_all, hist_err, bins, j, errs_j, errs_cumul, outfile):
    # Write simulation stats for iteration i to the given file.
    outfile.write("iteration: %d\n" % (j+1))
    outfile.write("errors for iteration: %d\tcumulative errors: %d\n" % (errs_j, errs_cumul))
    outfile.write("log-odds-bin\ttotal-phased\ttotal-incorrect\teffective-error-rate\n")
    for i in range(len(hist_all)):
            err_rate = -1
            if hist_all[i] > 0:
                err_rate = hist_err[i]/hist_all[i]
            outfile.write("%.5f\t%d\t%d\t%.5f\n" % (bins[i], hist_all[i], hist_err[i], err_rate))
    outfile.write("\n")
    

def combine_hists_and_bins(hist_all, hist_all_i, hist_err, hist_err_i, bins, bins_i, log_likelihood_ratio_interval):
    if len(bins_i) > len(bins):
        bins = np.append(bins, np.arange(max(bins),
                                         max(bins_i)+log_likelihood_ratio_interval,
                                         log_likelihood_ratio_interval)
        )
        hist_all = sum_unequal_hists(hist_all, hist_all_i)
        hist_err = sum_unequal_hists(hist_err, hist_err_i)
    elif len(bins) > len(bins_i):
        hist_all = sum_unequal_hists(hist_all_i, hist_all)
        hist_err = sum_unequal_hists(hist_err_i, hist_err)
    else:
        hist_all = hist_all + hist_all_i
        hist_err = hist_err + hist_err_i
        
    return hist_all, hist_err, bins


def sum_unequal_hists(shorter_arr, longer_arr):
    """
    Return the sum of two numpy histograms with different maximum bins.
    """
    return longer_arr + np.append(shorter_arr, np.zeros(len(longer_arr) - len(shorter_arr)))


def simulate_results_for_iteration(input_data, haplotypes, haplotype_specific_fasta, args):
    """
    Simulate data for a single iteration and tabulate results.
    """
    hist_all = np.array([])
    hist_err = np.array([])
    bins = np.array([])
    error_lr_list = []
    error_read_list = []
    for haplotype in haplotypes:
        sys.stderr.write("Simulating reads for haplotype %d...\n" % (haplotype))
        simulated_fastq = simulate_data(haplotype_specific_fasta[haplotype-1],
                                        args.simulation_error_model,
                                        args.output_directory_path+'/simulated_reads/',
                                        args.one_sample,
                                        haplotype,
                                        quiet = args.quiet_mode,
                                        silent = args.silent_mode)
        try:
            sys.stderr.write("Aligning simulated reads to reference genome...\n")
            input_data.add_reads(simulated_fastq,
                                 sample = args.one_sample,
                                 reference_sequence_input = args.reference_genome,
                                 clobber=True, quiet = args.quiet_mode,
                                 silent = args.silent_mode
            )
        except Exception as e:
            sys.stderr.write("%s\n" % e)
            continue

        
        # Extract log-likelihood ratios and phasing results for properly-mapped reads with >= min_het_sites
        sys.stderr.write("Phasing simulated reads...\n")
        hist_all_i, hist_err_i, bins_i, error_lr_list_i, error_read_list_i = parse_simulated_data(input_data, args)
        for j in range(len(error_lr_list_i)):
            error_lr_list.append(error_lr_list_i[j])
            error_read_list.append(error_read_list_i[j])
            
        if haplotype > 1:
            # Combine with results from other haplotype(s)
            hist_all, hist_err, bins = combine_hists_and_bins(hist_all, hist_all_i,
                                                              hist_err, hist_err_i,
                                                              bins, bins_i,
                                                              args.log_likelihood_ratio_interval
	    )
        else:
            hist_all, hist_err, bins = (hist_all_i, hist_err_i, bins_i)

        # Clean up after ourselves.
        os.remove(simulated_fastq)
        input_data._purge_alignment_files()
        sys.stderr.write("Done.\n")
        
    return hist_all, hist_err, bins, error_lr_list, error_read_list


def simulate_data(haplotype_specific_fasta, simulation_model,
                  output_directory, sample, haplotype,
                  depth = 1,
                  difference_ratio = '23:31:46', length_mean = 25000,
                  length_max = 1000000, length_min = 100, length_sd = 20000,
                  accuracy_min = 0.01, accuracy_max = 1.00,
                  accuracy_mean = 0.80,
                  quiet = False, silent = False):
    """
    Simulate reads for a single sample and haplotype.
    TO-DO: Make all optional args accessible as command-line options.
    """
    simulated_fastq = simulate_reads_pbsim2(
        reference_sequence = haplotype_specific_fasta,
        depth = depth,
        simulation_mode = simulation_model,
        difference_ratio = difference_ratio,
        length_mean = length_mean,
        length_max = length_max,
        length_min = length_min,
        length_sd = length_sd,
        accuracy_min = accuracy_min,
        accuracy_max = accuracy_max,
        accuracy_mean = accuracy_mean,
        output_directory = output_directory,
        sample = sample,
        haplotype = haplotype,
        quiet = quiet,
        silent = silent)
    
    return simulated_fastq


def parse_simulated_data(input_data, args):
    """
    Takes simulated alighments and parses out log-likelihood ratios and associated error counts.
    """
    log_ratios = []
    is_phased_correctly = []
    error_lr_list = []
    error_read_list = []
    for phasable_sample in input_data:
        # To-Do: Work in ability to select/ignore specific samples
        for alignment in phasable_sample:
            phased_read = PhasedRead(alignment, vcf_file = phasable_sample.vcf_file_path, sample = 'HG001', evaluate_true_alignment = True)
            if phased_read.alignment_is_mapped and phased_read.matches_true_alignment and phased_read.is_phased and int(phased_read.aligned_segment.get_tag('HS')) > 1:
                log_ratios.append(phased_read.log_likelihood_ratio)
                is_phased_correctly.append(phased_read.is_phased_correctly)
                if not phased_read.is_phased_correctly:
                    #sys.stderr.write("%s\n%s\n" % (phased_read, phased_read.is_phased_correctly))
                    error_lr_list.append(phased_read.log_likelihood_ratio)
                    error_read_list.append(phased_read)
        
    # Tabulate the total counts and number of errors at each log-odds level (binned in steps of bin_width).
    log_ratios = np.array(log_ratios)
    is_phased_correctly = np.array(is_phased_correctly, dtype=bool)
    bins = np.arange(0, np.ceil(max(log_ratios))+args.log_likelihood_ratio_interval, args.log_likelihood_ratio_interval)
    hist_all, edges = np.histogram(log_ratios, bins)
    hist_err, edges = np.histogram(log_ratios[np.nonzero(np.where(is_phased_correctly, is_phased_correctly == False, 1))], bins)
    
    return hist_all, hist_err, bins, error_lr_list, error_read_list


def getArgs() -> object:
    """Parses arguments:"""
    ################################################################################################################
    ############## LRphase Arguments ###############################################################################
    
    lrphase_parser: ArgumentParser = ArgumentParser(
        prog = 'LRphase', description = 'Tools for phasing individual long reads using haplotype information.'
    )
    
    lrphase_parser.add_argument('--version', action = 'version', version = __version__)

    lrphase_subparsers: _SubParsersAction = lrphase_parser.add_subparsers(
        title = '[LRphase modes]', dest = 'mode', description = 'Choose which mode to run:',
        help = 'mode must be added as first argument (ex: LRphase phasing)', required = True
    )

    
    ################################################################################################################
    ############## Phasing Mode Arguments ##########################################################################
    
    phasing_parser: ArgumentParser = lrphase_subparsers.add_parser(
        'phasing', description = "Tool for phasing individual long reads using haplotype information."
    )
    
    ############## Phasing Mode Required Arguments ##############
    phasing_parser_required: _ArgumentGroup = phasing_parser.add_argument_group('Required', 'Required for phasing')
    
    phasing_parser_required.add_argument(
        '-o', '--output_directory_name', required = True,
        help = 'Name given to directory where results will be output (ex: -o minion_GM12878_run3_phasing_output)',
        dest = 'output_directory_name', metavar = "</path/to/output>"
    )
    
    phasing_parser_required.add_argument(
        '-v', '--vcf', required = True,
        help = 'Path to vcf file with haplotype information that will be used for phasing. (Must be in .vcf.gz format '
        'with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and '
        'available on PATH because LRphase will attempt to convert it.  EX: -v GM12878_haplotype.vcf.gz)',
        dest = 'vcf_file_name', metavar = '<VCF_FILE>'
    )
    
    phasing_parser_required.add_argument(
        '-i', required = True,
        help = 'Path to alignment file (.bam or .sam) of long reads that will be used for phasing. If either a .sam '
        'file is provided or an index is not found, .sam and .bam file will be sorted and indexed using pysam. '
        'Sorted.bam files should be in same directory as their index (.sorted.bam.bai). EX: -a '
        'data/minion_GM12878_run3.sorted.bam, -i minion_GM12878_run3.sam) Path to long read file in .fastq '
        'format that will be used for alignment and phasing (ex: -i minion_GM12878_run3.fastq)',
        #dest = 'long_read_inputs', metavar = 'long-read input file', action = 'append', nargs = '*'
        dest = 'long_read_inputs', metavar = '<SAM/BAM/FASTQ>'
    )
    
    phasing_parser_required.add_argument(
        '-r', '--reference', required = False,
        help = 'Path to reference genome sequence file. REQUIRED if -i is used to specify reads in fastq format to be '
        'aligned prior to phasing. (file types allowed: .fa, .fna, fasta. EX: -r data/reference_hg38.fna)',
        dest = 'reference_genome', metavar = '<REF_FASTA>'
    )
    
    phasing_parser_required.add_argument(
        '-A', '--reference_assembly', required = False, default="hg38",
        help = 'Assembly for the reference genome. EX: -A hg38.',
        dest = 'reference_assembly', metavar = '<ASSEMBLY_NAME>'
    )

    phasing_parser_required.add_argument(
	'-t', '--threads', type=int, required=False, default=3,
        help = 'Number of threads to use for mapping step.',
        dest = 'threads', metavar = '<THREADS>'
    )
    
    ############## Phasing Mode Output Options ##############
    phasing_parser_output: _ArgumentGroup = phasing_parser.add_argument_group(
        'Output options', 'Options for tagging reads and printing output BAM files.'
    )

    phasing_parser_output.add_argument(
        '-H', '--omit_phasing_tag',
        help = 'Do not tag reads with "HP:i:1" (maternal) and "HP:i:2" (paternal) tags to indicate phase assignments.',
        dest = 'add_phasing_tag_to_output', action = 'store_false'
    )
    
    phasing_parser_output.add_argument(
        '-P', '--omit_phase_set_tag',
        help = 'Do not tag reads with "PS:i:x" tags, which label reads according to the phase set that was indicated in the vcf record used to assign a read to a phase.',
        dest = 'add_phase_set_tag_to_ouput', action = 'store_false'
    )

    phasing_parser_output.add_argument(
        '-Q', '--omit_phasing_quality_tag',
        help = 'Do not tag reads with "PC:i:x" tags, where x is an estimate of the accuracy of the phasing assignment in phred-scale.',
        dest = 'add_phasing_quality_tag_to_output', action = 'store_false'
    )

    phasing_parser_output.add_argument(
        '-O', '--output_mode', type=str, required=False, default="combined",
        choices=['combined', 'phase_tagged', 'full'],
        help = 'Specify whether/how phased, unphased, and nonphasable reads are printed to output. Modes available:\n\tcombined: All reads will be written to a common output file. The phasing tag (HP:i:N) can be used to extract maternal/paternal phased reads, unphased reads, and nonphasable reads.\n\tphase_tagged: Phased reads for both maternal and paternal phases will be written to a single output file, while unphased and nonphasable reads will be written to their own respective output files.\n\tfull: Maternal, paternal, unphased, and nonphasable reads will be printed to separate output files.',
        action = 'store'
    )
    
    ############## Multiple sample handling/phase set options for phasing mode ##############
    phasing_parser_multiple_sample = phasing_parser.add_argument_group(
        'Sample options',
        'Phasing options for files containing multiple samples or haplotypes. By default the input files are assumed '
        'to belong to the same haplotype and from the same sample. '
    )
    
    # phasing_parser_multiple_sample.add_argument('-R', '--add_read_group_tag_to_input_reads', required = False,
    # help='Use the --add_read_group_tag_to_input_reads option to overwrite or add @RG ID:Z:x SM:Z:y DS:Z:z headers
    # and RG:Z:x tags to all input reads where x is the ID number, y is the name of the sample to which the read
    # belongs, and z is a description of the experimental sample that generated the reads. (-R x y z)', nargs = 3,
    # dest = 'add_read_group_tag_to_input_reads')
    
    phasing_parser_multiple_sample.add_argument(
        '-s', '--one_sample', required = False,
        help = 'Use the --one_sample option to phase a specific sample present in the input reads and vcf file. (-s '
        'HG001)',
        metavar = '<SAMPLE_NAME>'
    )
    
    phasing_parser_multiple_sample.add_argument(
        '--ignore_samples',
        help = 'Use the --ignore_samples option to ignore sample labels. The first sample column in the VCF will be '
        'used and reads will not be matched using RG tags, samples, or phase sets.',
        action = 'store_true'
    )

    """
    # ############## Additional methods for evaluating phasing accuracy using simulated reads  ##############
    # Deprecated options? This functionality is now in error_analysis mode.

    # phasing_parser_simulation = phasing_parser.add_argument_group('Evaluation of phasing using simulated reads', 'Simulated reads are used to estimate the accuracy of phasing decisions and assign quality scores.')
    
    # phasing_parser_simulation.add_argument('--simulated', help='Use the --simulated option to enable extra analysis to be performed for determining correct phasing rates and selecting thresholds through iteration of phasing decisions over log likelihood thresholds 0-10. When --simulated is used, LRphase will skip phasing and process a per_read_phasing_stats.tsv results file located in the output folder specified by -o. ', action='store_true')
    
    # phasing_parser_simulation.add_argument('--simulated_bam', required = False, help = 'Path to file with phased reads to output results from simulated analyses.', dest = 'simulated_bam', metavar = 'phased output bam file')
    
    # phasing_parser_simulation.add_argument('--simulated_analysis_only', help='Use the --simulated option to enable extra analysis to be performed for determining correct phasing rates and selecting thresholds through iteration of phasing decisions over log likelihood thresholds 0-10.', action='store_true')
    
    # phasing_parser_simulation.add_argument('--simulated_phasing_stats', required = False, help = 'Path to file with phased reads to output results from simulated analyses.', dest = 'simulated_phasing_stats', metavar = 'phasing stats file')
    """
    
    ############## Statistical and error options for phasing mode ##############
    phasing_parser_stats_error: _ArgumentGroup = phasing_parser.add_argument_group(
        'Statistical options for phasing model',
        'Options to modify thresholds and error parameters involved in phasing decisions.'
    )

    phasing_parser_stats_error.add_argument(
        '--error_model', required = False, default = 0, choices = [0,1,2],
        help = 'Use the --error_model option to choose how to estimate sequencing error rates: 0: estimate per-base '
        'error rate as an average per read. 1: estimate per-base error rate locally around each het site. 2: '
        'Calculate per-base error rate using base quality scores (WARNING: do not use option 2 unless you are '
        'sure that the basecaller reported actual error rates). ',
        dest = 'error_model', type = int
    )

    """
    These options are disabled because the are not relevant to the current implementation of
    simulations through error_analysis mode.
    # phasing_parser_stats_error.add_argument('--read_average_error_model', help='Use the --read_average_error_model
    # option to estimate per-base error rate as an average per read.', action='store_false')
    
    #phasing_parser_stats_error.add_argument(
    #    '--error_stats',
    #    help = 'Use the --error_stats option to enable extra analysis to be performed for per-base error statistics.',
    #    action = 'store_true'
    #)
    
    #phasing_parser_stats_error.add_argument(
    #    '--phasing_error_file_path', required = False,
    #    help = "Path to file with estimated error statistics from simulated analyses.",
    #    dest = 'phasing_error_file_path', metavar = 'phasing_error_file_path'
    #)
    
    #phasing_parser_stats_error.add_argument(
    #    '--error_stats_hets', required = False,
    #    default = 'simulated_reads_log_likelihood_ratio_iteration_hets_phasing_stats.tsv',
    #    help = "'Path to file with estimated error statistics from simulated analyses.",
    #    dest = 'simulated_log_likelihood_ratio_iteration_hets_file', metavar = 'error statistics hets file'
    #)
    """

    phasing_parser_stats_error.add_argument(
        '-E', '--error_rate_threshold', type = float, required = False, default = 0.01,
        help = 'Error rate threshold on phasing results. This threshold equates to the estimated phasing error rate for an experiment, such that a threshold of 0.05 should be equivalent to a 5%% false-discovery rate. This rate is estimated based on a fitted power-law distribution with alpha and xmin parameters supplied with the --powlaw_alpha and --powlaw_xmin options. These parameters may be estimated by running the LRphase error_analysis mode.',
        dest = 'error_rate_threshold', metavar = '<MAX_ERROR_RATE>'
    )

    phasing_parser_stats_error.add_argument(
        '--log_likelihood_threshold', type = float, required = False, default = -1,
        help = 'Use a hard threshold on log-likelihood ratios instead of an error-rate threshold based on the fitted power-law distribution for error rates. Results will only be printed for predicted phasings with log-likelihood ratios equal to or greater than this threshold.',
        metavar = '<MIN_LIKELIHOOD_RATIO>'
    )

    phasing_parser_stats_error.add_argument(
        '--powlaw_alpha', type = float, required = False, default = 4.5,
        help = 'Alpha parameter for the fitted power law distribition used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 4.5',
        dest = 'powlaw_alpha', metavar="<ALPHA>"
    )

    phasing_parser_stats_error.add_argument(
        '--powlaw_xmin', type = float, required = False, default = 2.0,
        help = 'Xmin parameter for the fitted power law distrubution used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 2.0',
        dest = 'powlaw_xmin', metavar = '<XMIN>'
    )

    phasing_parser_stats_error.add_argument(
	'-q', '--quiet', help = 'Output to stderr from subprocesses will be muted.', action = 'store_true', dest = 'quiet_mode'
    )

    phasing_parser_stats_error.add_argument(
	'-S', '--silent', help = 'Output to stderr and stdout from subprocesses will be muted.', action = 'store_true', dest = 'silent_mode'
    )
    
    phasing_parser.set_defaults(func = phasing)


    #########################################################################################################################
    ############## Phasability Mode Arguments ###############################################################################
    
    phasability_parser = lrphase_subparsers.add_parser(
        'phasability',
        description = 'Tool that uses haplotype information as input and outputs predictions for how well LRphase will perform for a sequencing dataset with a given N50 and sequencing error rate. Phasability is defined as the probability of correctly phasing a read of width W that matches all variants in a single phase, calculated as (1 - empirical_phasing_error_rate) for any window of width W. Overlapping windows of width W are slid along the genome at intervals of step size S and results are reported in fixed-step wig format. Individual bins in the wig file describe phasability for the W-width window starting at the leftmost position of the bin.  Can be used to evaluate phasability genome-wide or at optional regions.'
    )
    
    ############## Phasability Mode Required Arguments ##############
    phasability_parser_required: _ArgumentGroup = phasability_parser.add_argument_group(
        'Required', 'Required for phasability analysis'
    )
    
    phasability_parser_required.add_argument(
        '-o', '--output_directory_name', required = True,
        help = 'Name given to directory where results will be output (ex: -o GM12878_phasability)',
        dest = 'output_directory_name', metavar = '</path/to/output>'
    )
    
    phasability_parser_required.add_argument(
        '-v', '--vcf', required = True,
        help = 'Path to vcf file with haplotype information that will be used for phasability analysis. (Must be in '
        '.vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be '
        'installed and available on PATH because LRphase will attempt to convert it. EX: -v '
        'GM12878_haplotype.vcf.gz)',
        dest = 'vcf_file_name', metavar = '<VCF_FILE>'
    )

    phasability_parser_required.add_argument(
        '-C', '--chrom_sizes', required = True, type=str,
        help = 'Chromosome sizes file. Required when using --autosomal_only',
        dest = 'chrom_sizes', metavar = '<CHROM_SIZES_FILE>'
    )
    
    ############## Phasability Mode Optional Arguments ##############
    phasability_parser_optional = phasability_parser.add_argument_group('Optional', 'Optional for phasability mode')
    
    phasability_parser_optional.add_argument(
        '-w', '--window_size', required = False, type=int, default = 25000,
        help = 'Window size for calculating phasability. Set this to a value near the N50 of the sequencing experiment you are evaluating. (default = 25000bp)',
        dest = 'window_size', metavar = '<N>'
    )
    
    phasability_parser_optional.add_argument(
        '-t', '--step_size', required = False, type = int, default = 1000,
        help = 'Distance between start positions of the overlapping windows used for phasability analysis (default = 1000bp)',
        dest = 'step_size', metavar = '<N>'
    )

    phasability_parser_optional.add_argument(
        '-e', '--sequencing_error_rate', required = False, type=float, default = 0.1,
        help = 'Estimaated per-base sequencing error rate. Typically ~0.1 for Nanopore sequencing. (Default = 0.1)',
        dest = 'sequencing_error_rate', metavar = '<ERROR_RATE>'
    )
    
    phasability_parser_optional.add_argument(
        '--powlaw_alpha', type = float, required = False, default = 4.5,
        help = 'Alpha parameter for the fitted power law distribition used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 4.5',
        dest = 'powlaw_alpha', metavar="<ALPHA>"
    )

    phasability_parser_optional.add_argument(
        '--powlaw_xmin', type = float, required = False, default = 2.0,
        help = 'Xmin parameter for the fitted power law distrubution used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 2.0',
        dest = 'powlaw_xmin', metavar = '<XMIN>'
    )
    
    phasability_parser_optional.add_argument(
        '-R', '--regions', required = False, type=str,
        help = 'Regions in which to estimate phasability, in BED format.',
        dest = 'regions', metavar = '<BED_FILE>'
    )
        
    phasability_parser_optional.add_argument(
        '-q', '--quiet', help = 'Output to stderr from subprocesses will be muted.', action = 'store_true', dest = 'quiet_mode'
    )

    phasability_parser_optional.add_argument(
	'-S', '--silent', help = 'Output to stderr and stdout from subprocesses will be muted.', action = 'store_true', dest = 'silent_mode'
    )
    
    phasability_parser.set_defaults(func = phasability)


    ##################################################################################################################
    ############## error_analysis Mode Arguments #####################################################################
    
    error_analysis_parser = lrphase_subparsers.add_parser(
        'error_analysis',
        description = 'Tool for estimating error rates in a dataset given a (set of) haplotype(s) and a reference genome. Simulated reads with known phase are generated based on the inputs, and processed through the LRphase phasing mode. Results are used to estimate parameters for the powerlaw distribution modeling empirical error rates within the data. (See https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0085777, and http://arxiv.org/abs/0706.1062 for more information.). Results of powerlaw model fittign are written to "simulation_error_model_output.txt" and a text report of error rates across the observed range of log-likelihood ratios is written to "simulation_error_stats.tsv" in the output directory. These files can be used to obtain the optimal parameters for setting thresholds for phasing mode: To use the fitted powerlaw model to set an error-rate based threshold (recommended), the "Fitted powerlaw alpha" and "Corrected powerlaw xmin" within "simulation_error_model_output.txt" represent the recommended values for the --powlaw_alpha and --powlaw_xmin options, respectively. This file also reports "Fitted powerlaw xmin", which is the actual xmin estimate from model fitting. This estimate tends to be systematically low, especially with fewer than 25,000 error observations, thus "Corrected powerlaw xmin" has been adjusted using a linear correction based on sample-size. If you are simulating more than 25,000 observations, you may wish to use the fitted value rather than the corrected value. To set a hard threshold on log-odds scores (NOT recommended), the values within "simulation_error_stats.tsv" can be used to build an eCDF from which a log-odds threshold can be chosen at any desired empirical error rate, which can be supplied to phasing mode using the --error_rate_threshold option.'
    )
    
    ############## error_analysis Mode Required Arguments ##############
    
    error_analysis_parser_required: _ArgumentGroup = error_analysis_parser.add_argument_group(
        'Required', 'Required for error_analysis'
    )
    
    error_analysis_parser_required.add_argument(
        '-o', '--output_directory_path', required = True,
        help = 'Name given to directory where results will be output (ex: -o minion_GM12878_run3_phasing_output)',
        dest = 'output_directory_path', metavar = '</path/to/output_directory>'
    )
    
    error_analysis_parser_required.add_argument(
        '-v', '--vcf', required = True,
        help = 'Path to vcf file with haplotype information that will be used for error_analysis. (Must be in .vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and available on PATH because LRphase will attempt to convert it.  EX: -v GM12878_haplotype.vcf.gz)',
        dest = 'vcf_file_path', metavar = '<VCF_FILE>'
    )

    error_analysis_parser_required.add_argument(
        '-p', '--simulation_error_model', required = True,
        help = 'Path to the error model for simulated sequence generation',
        dest = 'simulation_error_model', metavar = '<ERROR_MODEL_FILE>'
    )
    
    error_analysis_parser_required.add_argument(
        '-r', '--reference', required = True,
        help = 'Path to reference genome sequence file.',
        dest = 'reference_genome', metavar = '<GENOME_FASTA>'
    )

    error_analysis_parser_required.add_argument(
        '-A', '--reference_assembly', required = False, default='hg38', type=str,
        help = 'Reference genome assembly, e.g., hg38.',
        dest = 'reference_assembly', metavar = '<ASSEMBLY_NAME>'
    )

    error_analysis_parser_required.add_argument(
        '-t', '--threads', type=int, required=False, default=3,
        help = 'Number of threads to use for mapping step.',
        dest = 'threads', metavar='<N>'
    )
    
    ############## Additional methods for evaluating phasing accuracy using simulated reads  ##############
    error_analysis_parser_simulation: _ArgumentGroup = error_analysis_parser.add_argument_group(
        'Evaluation of phasing using simulated reads',
        'Simulated reads are used to estimate the accuracy of phasing decisions and assign quality scores.'
    )

    error_analysis_parser_simulation.add_argument(
        '--ignore_phase_set',
        help = 'Compare the quality scores in a phased bam to error rates determined from simulated reads. All input '
        'must be phased bam files that  -i for ath to phased with phased reads to output results from '
        'simulated analyses.',
        action = 'store_true'
    )

    error_analysis_parser_simulation.add_argument(
        '-l', '--log_likelihood_ratio_interval', required = False, type=float, default = 0.5,
        help = 'Bin width for tracking phasing error at each log-likelihood-ratio level.',
        dest = 'log_likelihood_ratio_interval', metavar = '<N>'

    )

    error_analysis_parser_simulation.add_argument(
	'--simulation_depth', required = False, default=25, type=int,
        help = 'Total read depth coverage for all simulations.',
        dest = 'simulation_depth', metavar = '<N>'
    )

    error_analysis_parser_simulation.add_argument(
	'--simulation_min_err_obs', required = False, default=-1, type=int,
        help = 'Minimum number of error observations to require before stopping simulations. It is recommended that this be set >= 1000 for reliable estimation of the xmin parameter, though as few as 50 observations is sufficient to reliably estimate alpha if xmin is already known.',
        dest = 'simulation_min_err_obs', metavar = '<N>'
    )

    error_analysis_parser_simulation.add_argument(
        '--sample', required = False, type=str,
        help = 'Sample name in VCF to use for haploytpe simulation.',
        dest = 'one_sample', metavar = '<SAMPLE_NAME>'
    )

    error_analysis_parser_simulation.add_argument(
        '--ignore_samples', required = False,
        help = 'Ignore VCF samples. Simulations will be based on all samples.',
        dest = 'ignore_samples', action='store_true'
    )

    error_analysis_parser_simulation.add_argument(
        '--autosomal_only', required = False,
        help = 'Only simulate sequences on autosomes.',
        dest = 'autosomal_only', action='store_true'
    )

    error_analysis_parser_simulation.add_argument(
        '--chrom_sizes', required = False, type=str,
        help = 'Chromosome sizes file. Required when using --autosomal_only',
        dest = 'chrom_sizes', metavar = '<FILE>'
    )

    error_analysis_parser_simulation.add_argument(
        '--store_error_probs', required = False,
        help = 'Write the list of likelihood ratios for all error observations to a comma-delimited text file.',
        dest = 'store_error_probs', action='store_true'
    )

    error_analysis_parser_required.add_argument(
        '--save_detailed_read_stats', default=False,
        help = 'Save detailed information on simulated error reads. Data will be stored to <output_dir>/error_read_stats.txt',
        dest = 'save_read_stats', action = 'store_true'
    )

    error_analysis_parser_required.add_argument(
        '--store_simulation_data_for_iterations', default=False,
        help = 'Save simulated error stats for each iteration to disk. Data will be stored to <output_dir>/per_iteration_simulation_error_stats.tsv',
        dest = 'store_simulation_data_for_iterations', action = 'store_true'
    )

    error_analysis_parser_simulation.add_argument(
	'-q', '--quiet', help = 'Output to stderr from subprocesses will be muted.', action = 'store_true', dest = 'quiet_mode'
    )

    error_analysis_parser_simulation.add_argument(
	'-S', '--silent', help = 'Output to stderr and stdout from subprocesses will be muted.', action = 'store_true', dest = 'silent_mode'
    )
    
    """
    # Args not used in the current implementation...
    # error_analysis_parser_simulation.add_argument('--evaluate_phased_bam', help = 'Compare the quality scores in a
    # phased bam to error rates determined from simulated reads. All input must be phased bam files that  -i for ath
    # to phased with phased reads to output results from simulated analyses.', action='store_true')
    # error_analysis_parser_simulation.add_argument('--simulated_bam', required = False, help = 'Path to file with
    # phased reads to output results from simulated analyses.', dest = 'simulated_bam', metavar = 'phased output bam
    # file')
    # error_analysis_parser_simulation.add_argument('--simulated_analysis_only', help='Use the --simulated option to
    # enable extra analysis to be performed for determining correct phasing rates and selecting thresholds through
    # iteration of phasing decisions over log likelihood thresholds 0-10.', action='store_true')
    # error_analysis_parser_simulation.add_argument('--simulated_phasing_stats', required = False, help = 'Path to
    # file with phased reads to output results from simulated analyses.', dest = 'simulated_phasing_stats',
    # metavar = 'phasing stats file')
    #error_analysis_parser_simulation.add_argument(
    #    '--evaluate_phasing_stats',
    #    help = 'Compare the quality scores in a phased bam to error rates determined from simulated reads. All input '
    #    'must be phased bam files that  -i for ath to phased with phased reads to output results from '
    #    'simulated analyses.',
    #    action = 'store_true'
    #)
    #error_analysis_parser_simulation.add_argument(
    #    '-I', '--input_simulated', required = False,
    #    help = "Path to file with phased reads to output results from simulated analyses.",
    #    dest = 'input_simulated',
    #    metavar = 'phasing stats file', action = 'append', nargs = '*'
    #)
    #error_analysis_parser_simulation.add_argument(
    #    '-s', '--sample_output', required = False,
    #    help = "Path to file with phased reads to output results from simulated analyses.", dest = 'sample_output',
    #    metavar = '<FILE>'
    #)
    #error_analysis_parser_simulation.add_argument(
    #    '-P', '--phase_set_output', required = False, default = 'NA',
    #    help = 'Path to file with phased reads to output results from simulated analyses.',
    #    dest = 'phase_set_output',
    #    metavar = "<FILE>"
    #)
    #error_analysis_parser_simulation.add_argument(
    #    '-L', '--log_likelihood_ratio_threshold', required = False, default = 2.0,
    #    help = 'Path to file with phased reads to output results from simulated analyses.',
    #    dest = 'log_likelihood_ratio_threshold', metavar = 'phase set to analyze'
    #)
    #error_analysis_parser_simulation.add_argument(
    #    '-E', '--error_rate_threshold', required = False, default = 0.05,
    #    help = 'error rate used for phasing decision',
    #    dest = 'error_rate_threshold', type = float, metavar = 'error rate threshold'
    #)
    #error_analysis_parser_simulation.add_argument(
    #    '--phasing_error_file_path', required = False,
    #    help = 'Path to file with estimated error statistics from simulated analyses.',
    #    dest = 'phasing_error_file_path', metavar = 'phasing_error_file_path'
    #)
    """
    
    error_analysis_parser.set_defaults(func = error_analysis)

    
    #####################################################################################################################
    ############## Parse arguments ######################################################################################    
    args = lrphase_parser.parse_args()
    args.func(args)    
    return args


def main():
    # This only needs to call the getArgs method, which will then dispatch functions for the indicated runtime mode.
    args: Namespace = getArgs()
    
    
if __name__ == '__main__':
    main()
