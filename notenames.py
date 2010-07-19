"""
notenames.py: Human-readable and shorthand note name to MIDI note number
mappings.
"""

# Note names and numbers taken from the GM1 Sound Set
# http://www.midi.org/techspecs/gm1sound.php
# and the GM2 Sound Set
# http://en.wikipedia.org/wiki/General_MIDI_Level_2#Drum_sounds
GM_SPEC_NOTE_NAME_TO_NUMBER_MAP = {
    # Cymbals
    'Crash Cymbal 1'     : 49,
    'Crash Cymbal 2'     : 57,
    'Ride Cymbal 1'      : 51,
    'Ride Cymbal 2'      : 59,
    'Ride Bell'          : 53,
    'Splash Cymbal'      : 55,
    'Chinese Cymbal'     : 52,
    # Toms
    'High Tom'           : 50,
    'Hi-Mid Tom'         : 48,
    'Low-Mid Tom'        : 47,
    'Low Tom'            : 45,
    'High Floor Tom'     : 43,
    'Low Floor Tom'      : 41,
    # Hi Hat
    'Closed Hi-Hat'      : 42,
    'Open Hi-Hat'        : 46,
    'Pedal Hi-Hat'       : 44,
    # Bass Drum
    'Acoustic Bass Drum' : 35,
    'Bass Drum 1'        : 36,
    # Snare
    'Acoustic Snare'     : 38,
    'Electric Snare'     : 40,
    # Misc
    'Hi Bongo'           : 60,
    'Side Stick'         : 37,
    'Low Bongo'          : 61,
    'Mute Hi Conga'      : 62,
    'Hand Clap'          : 39,
    'Open Hi Conga'      : 63,
    'Low Conga'          : 64,
    'High Timbale'       : 65,
    'Low Timbale'        : 66,
    'High Agogo'         : 67,
    'Low Agogo'          : 68,
    'Cabasa'             : 69,
    'Maracas'            : 70,
    'Short Whistle'      : 71,
    'Long Whistle'       : 72,
    'Short Guiro'        : 73,
    'Long Guiro'         : 74,
    'Claves'             : 75,
    'Hi Wood Block'      : 76,
    'Low Wood Block'     : 77,
    'Tambourine'         : 54,
    'Mute Cuica'         : 78,
    'Open Cuica'         : 79,
    'Cowbell'            : 56,
    'Mute Triangle'      : 80,
    'Open Triangle'      : 81,
    'Vibraslap'          : 58,
    # Additional GM2 Drum Sounds
    'High Q'             : 27,
    'Slap'               : 28,
    'Scratch 1'          : 29,
    'Scratch 2'          : 30,
    'Sticks'             : 31,
    'Square'             : 32,
    'Metronome 1'        : 33,
    'Metronome 2'        : 34,
    'Shaker'             : 82,
    'Jingle Bell'        : 83,
    'Belltree'           : 84,
    'Castanets'          : 85,
    'Mute Surdo'         : 86,
    'Open Surdo'         : 87,
}


DEFAULT_NOTE_NAME_TO_NUMBER_MAP = {
    'B'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Acoustic Bass Drum'],
    'C'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Crash Cymbal 1'],
    'C1' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Crash Cymbal 1'],
    'CC' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Crash Cymbal 1'],
    'f'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['High Floor Tom'],
    'F'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Low Floor Tom'],
    'F1' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['High Floor Tom'],
    'F2' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Low Floor Tom'],
    'H'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Closed Hi-Hat'],
    'Hf' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Pedal Hi-Hat'],
    'HH' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Closed Hi-Hat'],
    'R'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Ride Cymbal 1'],
    'Rd' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Ride Cymbal 1'],
    'S'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Acoustic Snare'],
    # Not sure about this
    't'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['High Tom'],
    'T'  : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Low Tom'],
    'T1' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['High Tom'],
    'T2' : GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Low Tom'],
}
