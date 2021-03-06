#!/usr/bin/env python3
"""
puma_poly run file

Authors: Josh Pace, Ken Youens-Clark, Koenraad Van Doorslaer
University of Arizona, KVD Lab & Hurwitz Lab
PuMA Poly 0.1 7/25/19 
"""

import argparse
import logging
import re
import os
import sys
import puma_poly


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)
# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)
# --------------------------------------------------
def get_args():
    args = sys.argv
    bin_dir = os.path.dirname(args[0])

    parser = argparse.ArgumentParser(
        description='Polyomavirus genome annotator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i',
                        '--input',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        help=('Path to a FASTA-formatted file that '
                              'contains a Polyomavirus genome.'),
                        required=True)

    parser.add_argument('-f',
                        '--format',
                        metavar='FORMAT',
                        choices=['fasta'],
                        default='fasta',
                        help='File format')

    parser.add_argument('-d',
                        '--data_dir',
                        metavar='DIR',
                        type=str,
                        default=os.path.join(bin_dir, 'data_dir_poly'),
                        help='Directory that has all database files for use')

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        type=str,
                        default=os.path.join(bin_dir, 'puma_poly_out'),
                        help='Output directory')

    parser.add_argument('-e',
                        '--evalue',
                        metavar='FLOAT',
                        type=float,
                        default=0.00001,
                        help='BLAST evalue')

    parser.add_argument('-m',
                        '--min_prot_len',
                        metavar='NUM',
                        type=int,
                        default=25,
                        help='Minimum protein length')

    parser.add_argument('-D',
                        '--debug_level',
                        metavar='STR',
                        type=str,
                        default='critical',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='Debug level')

    parser.add_argument('-l',
                        '--log_file',
                        metavar='FILE',
                        type=str,
                        default='puma_poly_execution.log',
                        help='Debug log file')

    args = parser.parse_args()

    if not os.path.isdir(args.data_dir):
        parser.error('--data_dir "{}" is not a directory.'.format(
            args.data_dir))

    return args
# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    args = vars(args)
    for_user_dir = os.path.join(args['out_dir'], 'for_user')
    if not os.path.isdir(for_user_dir):
        os.makedirs(for_user_dir)
    log_file = os.path.join(for_user_dir, args['log_file'])
    logging.basicConfig(level=level[args['debug_level']],
                        filename=log_file,
                        filemode='w')

    puma_poly.run(args)
    print("PuMA Poly execution complete. Check output files in {}. Also check "
          "puma_poly_execution.log for potential notes about execution.".format(
        for_user_dir))
# --------------------------------------------------
if __name__ == '__main__':
    main()

