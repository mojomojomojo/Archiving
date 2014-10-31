from soxutil import *

AUDIO            = segment(  211696,28601117)
AUDIO_01         = segment(  211696,20485497)
AUDIO_02         = segment(20553670,28601117)
TRAILING_SILENCE = segment(28611283,84860285)

NOISE_SAMPLES = segments(
    segment( 1346723, 1419680),
    segment( 5777991, 5946033),
    segment(20206823,20474733),
    segment(25280356,25413713),
)

NOISY_SEGMENTS = segments(
    segment( 4034201, 4628853),
    segment(14565037,15233870),
    segment(17914210,18971223), # quieter voices
)

