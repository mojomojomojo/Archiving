#!/usr/bin/env python3

import argparse
import subprocess
import os,re

from soxutil import *
import Tape001A


def build_cmdline():
    parser = argparse.ArgumentParser('audio fix for FWH_A1 Tape 1')
    parser.add_argument('files',type=str,nargs='*',default=[])
    parser.add_argument('--match',type=str,default=['Tape001.raw.A.composite'],nargs='*')
    parser.add_argument('--noisy',type=int,nargs='+',default=[0])
    parser.add_argument('--gain',type=float,help='amplify the audio by <n> dB')
    parser.add_argument('--normalize',type=float,help='normalize the audio to <n> dB below 0 dB (almost certainly negative)')
    return parser


def play( infile, segs, gain=None, normalize=None ):
    try:
        command = [
            'sox',
            '-q', # quiet
            infile,
            '-d',
            'trim' ] + segs.samples() + [
        ]
        if gain:
            command.extend(['gain',str(gain)])
        if normalize:
            command.extend(['gain','-n',str(normalize)])
        subprocess.call(command)
    except subprocess.CalledProcessError as e:
        print('Exception creating noise profile.\n{0}'.format(cpe_str(e)))
        raise e
    except Exception as e:
        print('Exception creating noise profile.')
        raise e


class PrefixMatch:
    def __init__(self,*prefixes):
        self.prefixes = list(prefixes)

    def match( self, fname ):
        for prefix in self.prefixes:
            try:
                if fname.index(prefix) == 0:
                    return True
            except ValueError:
                continue
        return False

if __name__ == '__main__':
    cmdline = build_cmdline().parse_args()

    wav = re.compile(r'\.wav$',re.I)
    targetFiles = PrefixMatch(*cmdline.match)
    playFiles = tuple(sorted(list(filter(targetFiles.match,
                                         filter(wav.search,os.listdir('.'))))+
                             cmdline.files))
    print('Comparing Files:\n  {0}\n'.format('\n  '.join(playFiles)))

    playSegments = segments(*[ Tape001A.NOISY_SEGMENTS[segIdx]
                               for segIdx in cmdline.noisy ])

    for afile in playFiles:
        print(afile)
        play(afile,playSegments,
             gain=cmdline.gain,
             normalize=cmdline.normalize)
