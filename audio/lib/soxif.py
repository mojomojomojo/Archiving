#!/usr/bin/env python3

'''
This class provides a utility wrapper around the redoubtable audio transform
utility, sox.

There's a better thought-out package: pysox
  https://pythonhosted.org/pysox/intro.html#simple-examples
This has some touchy prereqs, though, like the libsox binaries. It was also
  last modified on 2011-04-10 (3+ years ago).
This package is just an interface to the compiled executable.
'''

class Sox:
    '''
    A Sox object corresponds to an invocation of sox which operates
    on a single input file and optionally creates output files.
    '''

    # types
    SAMPLES = 1
    SECONDS = 2

    @classmethod
    def stream( cls, infile ):
        '''
        This is the expected entry point for instance creation.
        All sox operations start with an input file.
        '''
        return Sox(infile)


    # allow adding, subtracting, relative, absolute
    class Segment:
        '''
        This refers to a single segment of a clip. Internally, it represents
        all time positions as samples (for maximum precison)
        
        '''
        def __init__(self,_in,_out, units=Sox.SAMPLES, srate=44100,
                     relative=False):
            self.units = units
            self.srate = srate
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


    # allow indexing/slicing
    class SegmentList:
        '''
        A SegmentList is a series of segments that can be sliced like an
        list but also combined or otherwise operated upon in a manner that
        translates easily into parameters that sox likes.
        '''
        def __init__(self):
            pass

    class Chain:
        '''
        A chain refers to a single list of transforms that all apply to
        the same audio segment.

        You apply successive effects to a chain.
        '''
        def __init__(self,*args,**kwargs):
            self.effects = []

        def addEffect( self, effect, *args, **kwargs ):
            pass

    def __init__(self, infile=None, outfile=None):
        self.chains = []
        if infile:
            self.infile(infile)
        if outfile:
            self.outfile(outfile)

    def infile(self, infile):
        self._infile = infile
    def outfile(self, outfile):
        self._outfile = outfile

    def chain(self,*args,**kwargs):
        '''
        Add a new chain of effects for this object.
        '''
        c = Sox.Chain(*args,**kwargs)
        self.chains.append(c)
        return c

    def addEffect( self, effect, *args, **kwargs ):
        '''
        This is a shortcut to add an effect to the last chain in the list.
        If there isn't one, a new one is created and this effect is added
        to it.
        '''
        pass


    def flow(self):
        '''
        Apply all the chains to the input file, saving the result to
        the output file.
        '''
        if self._outfile:
            # Create a .info file with the executed command in it.
            pass
