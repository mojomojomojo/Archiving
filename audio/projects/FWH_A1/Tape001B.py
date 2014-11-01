from soxutil import *

# This tape came from an audio cassette.
# Labels:
#   Side A: "Stop 151 1-8-81 Betty + Mama"
#   Side B: "4-15-83 Me + Mama about Aunt Fanny"
# I digitized the audio before looking at the label. The raw recording
#   has side B first, then side A.


AUDIO            = segment( 93765221,113759787)
AUDIO_PIECES = segments(
    segment( 93765221,113759787),
)

TRAILING_SILENCE = segment(113799270,178413918)

# These are areas of relative silence where only the background noise
#   is audible.
NOISE_SAMPLES = segments(
    # AUDIO_PIECES[0]
    segment(100420086,100714640),
    segment(110574969,110662498),
)

# These are some segments chosen to test the noise reduction.
# They are either very noisy, difficult to understand, or at least
#   representative of noisy audio.
NOISY_SEGMENTS = segments(
    # AUDIO_PIECES[0]
    segment(113187138,113575310),
)

