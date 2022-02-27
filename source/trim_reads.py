'''
Author: Peng Liu
Date: 2022-02-17 22:17:10
LastEditTime: 2022-02-17 22:37:53
LastEditors: Please set LastEditors
Description: Trim read to special length.
FilePath: /circ_pipeline_test/Scripts/TrimReads.py
'''
#!/usr/bin/env python
import pysam
import numpy as np
import argparse
import os

def max_phred_based_idx(qual, window):
    """ Return index based quality window.  """
    assert len(qual) >= window
    step = len(qual) - window
    current_q, max_q, idx = 0, 0, 0
    for i in range(step):
        current_q = np.sum(qual[i:i+window])
        if current_q > max_q:
            max_q = current_q
            idx = i
        i += 1
    return idx

def bam_to_ubam(read, start:int=0, length:int=None):
    """ Convert BAM to uBAM record. """
    new_read = pysam.AlignedSegment()
    new_read.query_name = read.query_name 
    new_read.query_sequence = read.query_sequence[start:start+length]
    if read.is_read1:
        new_read.flag = 77
    else:
        new_read.flag = 141
    new_read.reference_id = -1 
    new_read.reference_start = -1
    new_read.mapping_quality = 0
    new_read.cigar = None
    new_read.next_reference_id = -1 
    new_read.next_reference_start = -1
    new_read.template_length = 0
    new_read.query_qualities = read.query_qualities[start:start+length]
    new_read.tags = (("YT", "UP"),)
    return new_read


def main():
    parser = argparse.ArgumentParser(description='Trimming and Convert to uBAM')
    parser.add_argument('bam', help='Input bam file.')
    parser.add_argument('-o', "--output", help='output file name.', type=str, default="./output.ubam")
    parser.add_argument('--keep-length', help='Sequence length for keeping.', type=int, default=145)
    args = parser.parse_args()

    outdir = os.path.dirname(args.output)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    
    header = { 'HD': {'VN': '1.0'}, 
           'SQ': [{'LN': 150, 'SN': 'PE150'},
                  {'LN': args.keep_length, 'SN': 'KEEP_LENGTH'}] 
         }

    # out_bam_file = args.prefix + "_trim_" + str(args.keep_length) + ".ubam"
    out_bam = pysam.AlignmentFile(args.output, "wb", header = header)

    with pysam.AlignmentFile(args.bam, 'rb') as in_bam:
        # index = pysam.IndexedReads(in_bam)
        # index.build()
        for read in in_bam.fetch(until_eof=True):
            if read.qlen >= args.keep_length:
                idx = max_phred_based_idx(read.query_qualities, args.keep_length)
                out_bam.write(bam_to_ubam(read, idx, args.keep_length))

    out_bam.close()

if __name__ == "__main__":
    main()
