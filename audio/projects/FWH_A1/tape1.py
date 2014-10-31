#!/usr/bin/env python3

'''
These are documented experiments to clean up the audio of one of the
archive audio cassettes.

Output files are always stored in the CWD.
'''

import subprocess
import argparse
import sys,os,os.path
from datetime import datetime,time

from soxutil import *
import Tape001A

class Timer:
    def __init__(self):
        self.start = datetime.now()
        self.end = None

    def stop(self):
        self.end = datetime.now()

    def __str__(self):
        if self.end:
            return str(self.end-self.start)
        else:
            return str(datetime.now()-self.start)

def build_cmdline():
    parser = argparse.ArgumentParser('audio fix for FWH_A1 Tape 1')
    parser.add_argument('file',type=str,default='Tape001.raw.wav')
    return parser

def cpe_str( cpe ):
    return 'Command: {0}\nOutput:\n{1}'.format(' '.join(cpe.cmd),cpe.output)

def remove_output( outfile ):
    if os.path.isfile(outfile):
        os.remove(outfile)

def noise_profile( infile, outfile, segs ):
    remove_output(outfile)
    try:
        output = subprocess.check_output(
            [
                'sox',
                infile,
                '-n', # to audio out
                'trim' ] + segs.samples() + [
                'noiseprof', outfile
            ],
            stderr = subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print('Exception creating noise profile.\n{0}'.format(cpe_str(e)))
        raise e
    except Exception as e:
        print('Exception creating noise profile.')
        raise e

def noise_reduce( infile, segs, outfile, profile, amount ):
    remove_output(outfile)
    try:
        output = subprocess.check_output(
            [
                'sox',
                infile,
                outfile,
                'trim' ] + segs.samples() + [
                'noisered', profile, str(amount),
            ],
            stderr = subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print('Exception with noise reduction.\n{0}'.format(cpe_str(e)))
        raise e
    except Exception as e:
        print('Exception with noise reduction.')
        raise e

    


def np_A_composite( infile ):
    infile_base = os.path.splitext(os.path.basename(infile))[0]

    profile = '{0}.A.composite.profile'.format(infile_base)
    print('Creating noise profile (A,composite): ',end='')
    sys.stdout.flush()
    timer = Timer()
    noise_profile(infile,profile,Tape001A.NOISE_SAMPLES)
    print(str(timer))

    # bracked the amounts (for comparison)
    for _amount in range(10,50,5):
        amount = _amount/100
        outfile = '{0}.A.composite-{1:03d}.wav'.format(infile_base,int(amount*100))
        print('Noise reduction: {0} ({1}): '.format(amount,outfile),end='')
        sys.stdout.flush()
        timer = Timer()
        noise_reduce(infile,Tape001A.AUDIO,outfile,profile,amount)
        print(str(timer))


if __name__ == '__main__':
    cmdline = build_cmdline().parse_args()

    timer = Timer()
    np_A_composite(cmdline.file)
    print('\n\nTotal Elapsed: {0}\n'.format(timer))
