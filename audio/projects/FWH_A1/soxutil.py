#!/usr/bin/env python3

import itertools

# Samples is the time format used here because it provides the maximum
#   resolution/precision.

class segment:
    def __init__(self,_in,_out,relative=False):
        self.i,self.o,self.rel = _in,_out,relative

    def seconds(self):
        return '{0} ={1}'.format(seconds(samples=self.i),
                                 seconds(samples=self.o))
    def samples(self):
        return ['={0}s'.format(self.i), '{0}s'.format(self.o-self.i)]
    
    def __str__(self):
        return 'Segment({0},{1})'.format(self.i,self.o)

    def __sub__(self, seg):
        return segment(self.i-seg.o, self.o-seg.o,relative=True)

class segments:
    def __init__(self,*segs):
        self.segments = tuple(segs)
    def samples(self):
        return list(itertools.chain.from_iterable(map(lambda s:s.samples(),self.segments)))
    def __getitem__(self,idx):
        return self.segments[idx]
    def __str__(self):
        return 'Segments[{0}]'.format(' '.join(list(map(str,self.segments))))
    def __len__(self):
        return  len(self.segments)

def seconds(sampRate=44100, samples=None, hms=None):
    '''
    Return a decimal number of seconds.
    '''
    if samples is not None:
        return samples/sampRate

    #untested
    if hms is not None:
        (time.strptime('%H:%M:%S',hms)-time()).total_seconds

