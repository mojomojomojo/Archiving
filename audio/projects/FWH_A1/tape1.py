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
import shlex, socket, getpass


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

def q( cmdstr ):
    return shlex.quote(cmdstr)

def sox( outfile, sox_cmd, descr=None ):
    remove_output(outfile)

    outinfo = '{0}.info'.format(outfile)
    remove_output(outinfo)
    with open(outinfo,'wt',encoding='utf-8') as info:
        print('# {0}'.format(' '.join(tuple(map(shlex.quote,sox_cmd)))),
              file=info)
        print('# invoked on {stamp} by {user} on {machine}'.format(
            stamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            user  = getpass.getuser(),
            machine = socket.gethostname(),
            ), file=info)

    startTime = datetime.now()
    exc = None # an exception to reraise
    try:
        subprocess.check_output( sox_cmd,
                                 stderr = subprocess.STDOUT )
    except subprocess.CalledProcessError as e:
        print('Exception {0}.\n{1}'.format(descr if descr else '',cpe_str(e)))
        exc = e
    except Exception as e:
        print('Exception {}'.format(descr if descr else ''))
        exc = e
    elapsed = datetime.now()-startTime

    with open(outinfo,'at',encoding='utf-8') as info:
        print('# Elapsed Time: {0}'.format(elapsed), file=info)

    if exc:
        raise exc
    

def noise_profile( infile, outfile, segs ):
    sox(outfile,
        [
            'sox',
            infile,
            '-n', # to audio out
            'trim' ] + segs.samples() + [
                'noiseprof', outfile
        ],
        'creating noise profile')


def noise_reduce( infile, segs, outfile, profile, amount ):
    sox(outfile,
        [
            'sox',
            infile,
            outfile,
            'trim' ] + segs.samples() + [
                'noisered', profile, str(amount),
        ],
        'using noise reduction filter')


def sox_xform( infile, outfile, xforms ):
    command = [
        'sox',
        infile,
        outfile,
    ]
    for i in range(len(xforms)):
        if i > 0:
            command.append(':')
        command.extend(xforms[i])

    sox(outfile,command,'applying transforms')



def np_A_composite( infile ):
    infile_base = os.path.splitext(os.path.basename(infile))[0]

    profiles = [ '{0}.A{1}.composite.profile'.format(infile_base,i)
                 for i in range(3) ]
    print('Creating noise profiles (A,composite): ',end='')
    sys.stdout.flush()
    timer = Timer()
    noise_profile(infile,profiles[0],
                  segments(Tape001A.NOISE_SAMPLES[0],
                           Tape001A.NOISE_SAMPLES[1]))
    noise_profile(infile,profiles[1],
                  segments(Tape001A.NOISE_SAMPLES[2],
                           Tape001A.NOISE_SAMPLES[3]))
    noise_profile(infile,profiles[2],
                  segments(Tape001A.NOISE_SAMPLES[4],
                           Tape001A.NOISE_SAMPLES[5]))
    print(str(timer))

    # bracked the amounts (for comparison)
    # 30/0: pretty clean
    # 50/0: noticeably muted
    for prof_idx in range(len(profiles)):
        for _amount in range(5,50,5):
            amount = _amount/100
            outfile = '{0}.A{2}.composite-{1:03d}.wav'.format(infile_base,int(amount*100),prof_idx)
            print('Noise reduction: {0} ({1}): '.format(amount,outfile),end='')
            sys.stdout.flush()
            timer = Timer()
            noise_reduce(infile,Tape001A.AUDIO,outfile,profiles[prof_idx],amount)
            print(str(timer))


def np_A_composite_finish( infile, outfile ):
    infile_base = os.path.splitext(os.path.basename(infile))[0]

    profiles = [ '{0}.A{1}.composite.profile'.format(infile_base,i)
                 for i in range(3) ]
    print('Creating noise profiles (A,composite): ',end='')
    sys.stdout.flush()
    timer = Timer()
    noise_profile(infile,profiles[0],
                  segments(Tape001A.NOISE_SAMPLES[0],
                           Tape001A.NOISE_SAMPLES[1]))
    noise_profile(infile,profiles[1],
                  segments(Tape001A.NOISE_SAMPLES[2],
                           Tape001A.NOISE_SAMPLES[3]))
    noise_profile(infile,profiles[2],
                  segments(Tape001A.NOISE_SAMPLES[4],
                           Tape001A.NOISE_SAMPLES[5]))
    print(str(timer))

    amounts = [ .3, .3, .3 ]

    xforms = []
    for i in range(len(profiles)):
        relseg = Tape001A.AUDIO_PIECES[i]
        if i > 0:
            relseg -= Tape001A.AUDIO_PIECES[i-1]
        xforms.append(['trim']+relseg.samples()+['noisered',profiles[i],str(amounts[i])])


    print('Applying finished noise reductions: ',end='')
    sys.stdout.flush()
    timer = Timer()
    sox_xform(infile,outfile,xforms)
    print(str(timer))


if __name__ == '__main__':
    cmdline = build_cmdline().parse_args()

    if not os.path.isfile(cmdline.file):
        print("Specified file does not exist: '{0}'".format(cmdline.file))
    timer = Timer()
    np_A_composite(cmdline.file)
#    np_A_composite_finish(cmdline.file,'test-finished.wav')
    print('\n\nTotal Elapsed: {0}\n'.format(timer))
