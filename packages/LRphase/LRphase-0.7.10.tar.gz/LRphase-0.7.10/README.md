# LRphase
## A tool for phasing long-read sequencing results.

LRphase phases long reads based on haplotype data in a VCF file.


## Dependencies
### All modes:
* HTSlib (https://www.htslib.org/)
* Python >= v3.7
* minimap2  (https://github.com/lh3/minimap2)
* numpy (https://numpy.org/)
* powerlaw (https://github.com/jeffalstott/powerlaw)
* pysam (https://github.com/pysam-developers/pysam)
* pyliftover (https://github.com/konstantint/pyliftover)

### Simulation mode
* pbsim2 (https://github.com/yukiteruono/pbsim2)


## Installation

We strongly recommend installing with conda, into a new environment:
```
conda create -n LRphase_env -c conda-forge -c bioconda numpy pysam powerlaw pyliftover pbsim2 minimap2 LRphase
```

Install with pip:
```
pip install LRphase
```

Installation from the github repository is not recommended. However, if you must, follow the steps below:
1) git clone https://github.com/Boyle-Lab/LRphase.git
2) cd LRphase/
3) python3.7 -m pip install -e .


## Usage

```
LRphase [-h] [--version] [-q] {phasing,phasability,error_analysis} ...
```

LRphase may be run in any of three modes:
1) Phasing mode: Assigns phase to individual long reads based on variants in a VCF file.
2) Error-Analysis mode: Uses simulated long-read data to estimate the error model parameters based on the given VCF file and reference sequence.
3) Phasability mode: Rapidly estimates phasability (1 - empirical_phasing_error_rate) for fixed-width windows spanning the genome or an optional regions file.

### Phasing Mode
Tool for phasing individual long reads using haplotype information.

```
LRphase phasing [-h] -o </path/to/output> -v <VCF_FILE> -i
                       <SAM/BAM/FASTQ> [-r <REF_FASTA>] [-A <ASSEMBLY_NAME>]
                       [-t <THREADS>] [-H] [-P] [-Q]
                       [-O {combined,phase_tagged,full}]
                       [-s <SAMPLE_NAME>]
                       [--ignore_samples] [--error_model {0,1,2}]
                       [-E <MAX_ERROR_RATE>]
                       [--log_likelihood_threshold <MIN_LIKELIHOOD_RATIO>]
                       [--powlaw_alpha <ALPHA>] [--powlaw_xmin <XMIN>]
```

#### Required Arguments
| Argument | Description |
|---|---|
| __-o </path/to/output>, --output_directory_name </path/to/output_directory>__ | Output directory name. Name given to directory where results will be output. |
| __-v <VCF_FILE>, --vcf <VCF_FILE>__ | Path to vcf file with haplotype information that will be used for phasing. (Must be in .vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and available on PATH because LRphase will attempt to convert it. |
| __-i <SAM/BAM/FASTQ>__ | Path to long reads (.fastq format) or alignment file (.bam or .sam) that will be used for phasing. If either a .sam file is provided or an index is not found, .sam and .bam file will be sorted and indexed using pysam. Sorted.bam files should be in same directory as their index (.sorted.bam.bai). |
| __-r <REF_FASTA>, --reference <REF_FASTA>__ | Path to reference genome sequence file. REQUIRED if argument to -i a fastq file. |
| __-A <ASSEMBLY_NAME>, --reference_assembly <ASSEMBLY_NAME>__ | Assembly for the reference genome. EX: -A hg38. |


#### Optional Arguments
| Argument | Description |
|---|---|
| __-h, --help__ | Show help message and exit |
| __-t <THREADS>, --threads <THREADS>__ | Number of threads to use for mapping step. |
| __-H, --omit_phasing_tag__ | Do not tag reads with "HP:i:1" (paternal) and "HP:i:2" (maternal) tags to indicate phase assignments. |
| __-P, --omit_phase_set_tag__ | Do not tag reads with "PS:i:x" tags, which label reads according to the phase set that was indicated in the vcf record used to assign a read to a phase. |
| __-Q, --omit_phasing_quality_tag__ | Do not tag reads with "PC:i:x" tags, where x is an estimate of the accuracy of the phasing assignment in phred-scale. ||
| __-O {combined,phase_tagged,full}, --output_mode {combined,phase_tagged,full}__ | Specify whether/how phased, unphased, and nonphasable reads are printed to output. Modes available: combined: All reads will be written to a common output file. The phasing tag (HP:i:N) can be used to extract maternal/paternal phased reads, unphased reads, and nonphasable reads. phase_tagged: Phased reads for both maternal and paternal phases will be written to a single output file, while unphased and nonphasable reads will be written to their own respective output files. full: Maternal, paternal, unphased, and nonphasable reads will be printed to separate output files. |
| __-s <SAMPLE_NAME>, --one_sample <SAMPLE_NAME>__ | Phase only a specific sample present in the input reads and vcf file. (-s HG001) |
| __--ignore_samples__ | Ignore sample labels in VCF. The first sample column in the VCF will be used and reads will not be matched using RG tags, samples, or phase sets. |
| __--error_model {0,1,2}__ | Choose how to estimate sequencing error rates: 0: (default) Estimate per-base error rate as an average per read. 1: estimate per-base error rate locally around each het site. 2: Calculate per-base error rate using base quality scores WARNING: do not use option 2 unless you are sure that the basecaller reported actual error rates). |
| __-E <MAX_ERROR_RATE>, --error_rate_threshold <MAX_ERROR_RATE>__ | Error rate threshold on phasing results. This threshold equates to the estimated phasing error rate for an experiment, such that a threshold of 0.05 should be equivalent to a 5% false-discovery rate. This rate is estimated based on a fitted power-law	distribution with alpha and xmin parameters supplied with the --powlaw_alpha and --powlaw_xmin options. These parameters may be estimated by running the LRphase error_analysis mode. |
| __--log_likelihood_threshold <LOG_LIKELIHOOD_THRESHOLD>__ | Use a hard threshold on log-likelihood ratios instead of an error-rate threshold based on the fitted power-law distribution for error rates. Results will only be printed for predicted phasings with log-likelihood ratios equal to or greater than this threshold. |
| __--powlaw_alpha <ALPHA>__ | Alpha parameter for the fitted power law distribition used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 4.5 |
| __--powlaw_xmin <XMIN>__ | Xmin parameter for the fitted power law distrubution used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 2.0 |


### Error-analysis mode
Tool for estimating error rates in a dataset given a (set of) haplotype(s) and
a reference genome. Simulated reads with known phase are generated based on
the inputs, and processed through the LRphase phasing mode. Results are used
to estimate parameters for the powerlaw distribution modeling empirical error
rates within the data. (See
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0085777, and
http://arxiv.org/abs/0706.1062 for more information.). Results of powerlaw
model fittign are written to "simulation_error_model_output.txt" and a text
report of error rates across the observed range of log-likelihood ratios is
written to "simulation_error_stats.tsv" in the output directory. These files
can be used to obtain the optimal parameters for setting thresholds for
phasing mode: To use the fitted powerlaw model to set an error-rate based
threshold (recommended), the "Fitted powerlaw alpha" and "Fitted powerlaw
xmin" within "simulation_error_model_output.txt" represent the recommended
values for the --powlaw_alpha and --powlaw_xmin options, respectively. To set
a hard threshold on log-odds scores (NOT recommended), the values within
"simulation_error_stats.tsv" can be used to build an eCDF from which a log-
likelihood ratio threshold can be chosen at any desired empirical error rate,
which can be supplied to phasing mode using the --error_rate_threshold option.

```
LRphase error_analysis [-h] -o </path/to/output_directory> -v
                              <VCF_FILE> -p <ERROR_MODEL_FILE>
                              -r <GENOME_FASTA> [-A <ASSEMBLY_NAME>]
                              [-t <N>] [--ignore_phase_set] [-l <N>]
                              [--simulation_depth <N>]
                              [--simulation_min_err_obs <N>]
                              [--sample <SAMPLE_NAME>] [--ignore_samples]
                              [--autosomal_only] [--chrom_sizes <FILE>]
```

#### Required Arguments
| Argument | Description |
|---|---|
| __-o </path/to/output_directory>, --output_directory_path </path/to/output_directory>__ | Name given to directory where results will be output (ex: -o minion_GM12878_run3_phasing_output) |
| __-v <VCF_FILE>, --vcf <VCF_FILE>__ | Path to vcf file with haplotype information that will be used for error_analysis. (Must be in .vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and available on PATH because LRphase will attempt to convert it. EX: -v GM12878_haplotype.vcf.gz) |
| __-p <ERROR_MODEL_FILE>, --simulation_error_model <ERROR_MODEL_FILE>__ | Path to the error model for simulated sequence generation. |
| __-r <GENOME_FASTA>, --reference <GENOME_FASTA>__ | Path to reference genome sequence file. |

#### Optional Arguments
| Argument | Description |
|---|---|
| __-h, --help__ | Show help message and exit |
| __-A <ASSEMBLY_NAME>, --reference_assembly <ASSEMBLY_NAME>__ | Reference genome assembly, e.g., hg38. |
| __-t <N>, --threads <N>__ | Number of threads to use for mapping step. |
| __--ignore_phase_set__ | Compare the quality scores in a phased bam to error rates determined from simulated reads. All input must be phased bam files that -i for ath to phased with phased reads to output results from simulated analyses. |
| __-l <N>, --log_likelihood_ratio_interval <N>__ | Bin width for tracking phasing error at each log-likelihood-ratio level. |
| __--simulation_depth <N>__ | Total read depth coverage for all simulations. |
| __--simulation_min_err_obs <N>__ | Minimum number of error observations to require before stopping simulations. It is recommended that this be set >= 1000 for reliable estimation of the xmin parameter, though as few as 50 observations is sufficient to reliably estimate alpha if xmin is already known. |
| __--sample <SAMPLE_NAME>__ | Sample name in VCF to use for haploytpe simulation. 
| __--ignore_samples__ | Ignore VCF samples. Simulations will be based on all samples. |
| __--autosomal_only__ | Only simulate sequences on autosomes. |
| __--chrom_sizes <FILE>__ | Chromosome sizes file. Required when using --autosomal_only |


### Phasability Mode
Tool that uses haplotype information as input and outputs predictions for how
well LRphase will perform for a sequencing dataset with a given N50 and
sequencing error rate. Phasability is defined as the probability of correctly
phasing a read of width W that matches all variants in a single phase,
calculated as (1 - empirical_phasing_error_rate) for any window of width W.
Overlapping windows of width W are slid along the genome at intervals of step
size S and results are reported in fixed-step wig format. Individual bins in
the wig file describe phasability for the W-width window starting at the
leftmost position of the bin. Can be used to evaluate phasability genome-wide
or at optional regions.

```
LRphase phasability [-h] -o </path/to/output> -v <VCF_FILE> -C
                           <CHROM_SIZES_FILE> [-w <N>] [-t <N>]
                           [-e <ERROR_RATE>] [--powlaw_alpha <ALPHA>]
                           [--powlaw_xmin <XMIN>] [-R <BED_FILE>] [-q]
```

#### Required Arguments
| Argument | Description |
|---|---|
| __-o </path/to/output>, --output_directory_name </path/to/output>__ | Name given to directory where results will be output ex: -o GM12878_phasability) |
| __-v <VCF_FILE>, --vcf <VCF_FILE>__ | Path to vcf file with haplotype information that will be used for phasability analysis. (Must be in .vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and available on PATH because LRphase will attempt to convert it. EX: -v GM12878_haplotype.vcf.gz) |
| __-C <CHROM_SIZES_FILE>, --chrom_sizes <CHROM_SIZES_FILE>__ | Chromosome sizes file. Required when using --autosomal_only |

#### Optional Arguments
| Argument | Description |
|---|---|
| __-h, --help__ | Show help message and exit |
| __-w <N>, --window_size <N>__ | Window size for calculating phasability. Set this to a value near the N50 of the sequencing experiment you are evaluating. (default = 25000bp) |
| __-t <N>, --step_size <N>__ | Distance between start positions of the overlapping windows used for phasability analysis (default = 1000bp) |
| __-e <ERROR_RATE>, --sequencing_error_rate <ERROR_RATE>__ | Estimaated per-base sequencing error rate. Typically ~0.1 for Nanopore sequencing. (Default = 0.1) |
| __--powlaw_alpha <ALPHA>__ | Alpha parameter for the fitted power law distribition used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 4.5 |
| __--powlaw_xmin <XMIN>__ | Xmin parameter for the fitted power law distrubution used in error-rate calculations. This can be obtained by running LRphase error_analysis mode. Default = 2.0 |
| __-R <BED_FILE>, --regions <BED_FILE>__ | Regions in which to estimate phasability, in BED format. |
| __-q, --quiet__ | stdout will be muted |
