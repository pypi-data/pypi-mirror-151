"""
Helper functions.
"""

import sys, os
import pysam

def is_gzip(filepath):
    """
    Test an input file for (likely) gzip format.
    """
    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'

    
def file_test(filepath, file_type=None, allow_gzip=False):
    """
    Test to see if filepath matches file_type given based on some nominal tests.
    """
    if not os.path.isfile(filepath):
        raise Exception('File %s does not exist.' % filepath)

    if file_type == None:
        return True
    else:
        fname = os.path.baseame(filepath)

        # gzip test only
        if file_type in ['gz' or 'gzip']:
            return is_gzip(filepath)

        # See if gzipped file is allowable and test file accordingly.
        if allow_gzip:
            fparts = os.path.splitext(fname)
            if fparts[1] in ['gz', 'gzip']:
                fname = fparts[0]
        else:
            if is_gzip(filepath):
                raise Exception('Gzip format not allowed.')

        # Fastq format test
        if file_type == 'fastq' and (str(fname).lower().endswith('.fastq') or str(fname).lower().endswith('.fq')):
            return True

        
        
    return False
