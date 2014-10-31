from soxutil import *

# This tape came from an audio cassette.
# Labels:
#   Side A: "Stop 151 1-8-81 Betty + Mama"
#   Side B: "4-15-83 Me + Mama about Aunt Fanny"
# I digitized the audio before looking at the label. The raw recording
#   has side B first, then side A.


AUDIO            = segment(  211696,28601117)
AUDIO_PIECES = segments(
    segment(  211696,17927836), # one volume level

    # The volume level decreases here. There's no obvious audible
    #   evidence of a stop-tape, movement, or other environmental
    #   adjustment that would cause it. The most obvious evidence is
    #   the quieting of the background hiss.
    segment(17927836,20490723), # 6:46 - 7:45

    # There's a stop-start artifact here.

    segment(20549329,28569837),

)
TRAILING_SILENCE = segment(28611283,84860285)

# These are areas of relative silence where only the background noise
#   is audible.
NOISE_SAMPLES = segments(
    # AUDIO_PIECES[0]
    segment( 1346723, 1419680),
    segment( 5777991, 5946033),
    # AUDIO_PIECES[1]
    segment(18280149,18351321),
    segment(20206823,20474733),
    # AUDIO_PIECES[2]
    segment(21404259,21507010),
    segment(25280356,25413713),
    segment(28099083,28234563),
)

# These are some segments chosen to test the noise reduction.
# They are either very noisy, difficult to understand, or at least
#   representative of noisy audio.
NOISY_SEGMENTS = segments(
    # AUDIO_PIECES[0]
    segment( 4034201, 4628853),
    segment(14565037,15233870),
    segment(17914210,18971223), # quieter voices
    # AUDIO_PIECES[1]
    segment(18300177,18969696), # Did mama and daddy teach her at home?
    # AUDIO_PIECES[2]
    segment(26990890,27561732),
    segment(27646977,28099083),
)

