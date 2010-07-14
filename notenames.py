"""
notenames.py: Human-readable and shorthand note name to MIDI note number
mappings.
"""

# Note names and numbers taken from the GM1 Sound Set
# http://www.midi.org/techspecs/gm1sound.php
# and the GM2 Sound Set
# http://en.wikipedia.org/wiki/General_MIDI_Level_2#Drum_sounds
GMSpecDrumNameToMidiNote = {
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


defaultNoteNameToNoteNumberMap = {
    'B'  : GMSpecDrumNameToMidiNote['Acoustic Bass Drum'],
    'C'  : GMSpecDrumNameToMidiNote['Crash Cymbal 1'],
    'C1' : GMSpecDrumNameToMidiNote['Crash Cymbal 1'],
    'CC' : GMSpecDrumNameToMidiNote['Crash Cymbal 1'],
    'f'  : GMSpecDrumNameToMidiNote['High Floor Tom'],
    'F'  : GMSpecDrumNameToMidiNote['Low Floor Tom'],
    'F1' : GMSpecDrumNameToMidiNote['High Floor Tom'],
    'F2' : GMSpecDrumNameToMidiNote['Low Floor Tom'],
    'H'  : GMSpecDrumNameToMidiNote['Closed Hi-Hat'],
    'Hf' : GMSpecDrumNameToMidiNote['Pedal Hi-Hat'],
    'HH' : GMSpecDrumNameToMidiNote['Closed Hi-Hat'],
    'R'  : GMSpecDrumNameToMidiNote['Ride Cymbal 1'],
    'Rd' : GMSpecDrumNameToMidiNote['Ride Cymbal 1'],
    'S'  : GMSpecDrumNameToMidiNote['Acoustic Snare'],
    # Not sure about this
    't'  : GMSpecDrumNameToMidiNote['High Tom'],
    'T'  : GMSpecDrumNameToMidiNote['Low Tom'],
    'T1' : GMSpecDrumNameToMidiNote['High Tom'],
    'T2' : GMSpecDrumNameToMidiNote['Low Tom'],
}
