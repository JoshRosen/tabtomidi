import string
from midiutil.MidiFile import MIDIFile
from notenames import defaultNoteNameToNoteNumberMap, GMSpecDrumNameToMidiNote


class TabParsingException(Exception):
    """
    Base class for all exceptions due to unparsable tabs.
    """

    def __init__(self, message, row=None, column=None):
        Exception.__init__(self, message)
        self.row = row
        self.column = column


class UnmappableNoteNamesException(TabParsingException):
    """
    Raised when the parser cannot map one or more note names to midi notes.
    The noteNames attribute provides the set of unmappable note names.
    """

    def __init__(self, noteNames):
        Exception.__init__(self,
            "Some note names could not be mapped to midi notes")
        self.noteNames = noteNames


class Tab(object):
    """
    Provides information about drum tabs and generates midi files from them.
    """

    def __init__(self, tabtext, noteNameToNoteNumberMap=defaultNoteNameToNoteNumberMap, bpm=100,
                 strikeVolume=70, accentVolume=110, ghostNoteVolume=50):
        """
        Constructs a Tab object from a string representing a tab.
        """
        self._tab = tabtext.splitlines()
        self._BPM = bpm
        self._strikeVolume = strikeVolume
        self._accentVolume = accentVolume
        self._ghostNoteVolume= ghostNoteVolume
        self._barRows = self._calculateBarRows()
        self._noteTypes = self._findAllNoteTypes()
        # Filter out notes from noteNameToNoteNumberMap that do not appear in this tab
        self._noteNameToNoteNumberMap = \
            dict((note, noteNameToNoteNumberMap[note]) for note in
            noteNameToNoteNumberMap.keys() if note in self._noteTypes)
        self.divisionsInBar = self._calculateDivisionsInBar(self._barRows[0])
        # Assuming that all bar have same number of divisions.
        # Some tabs have extra characters between the bars, i.e. 33 instead of
        # 32, so simply counting the number of characters between the bars will not
        # always work.
        # Also, some songs have half a bar of extra notes at the beginning.


    def writeMIDIFile(self, file):
        """
        Writes midi generated from this tab to the given file object.
        """
        # Throw an exception if there are note names for which we can't
        # determine the proper note numbers.
        unmappalbeNoteNames = self._noteTypes.difference(self._noteNameToNoteNumberMap.keys())
        if unmappalbeNoteNames:
            raise UnmappableNoteNamesException(unmappalbeNoteNames)

        tab = self._tab
        m = MIDIFile(1)
        track = 0
        time = 0
        channel = 9 # Should be channel 10; there may be an off-by-one error in midiutil
        duration = 4.0 / self.divisionsInBar # 4.0 is because midiutil's unit of time is the quarter note.
        m.addTrackName(track, time, "")
        m.addTempo(track, time, self._BPM)
        for r in self._barRows:
            # Determine whether the first row contains notes or repetition information.
            if not self._findNoteType(r):
                repSkip = 1
            else:
                repSkip = 0
            # Determine which drums are present in this group of bars.
            noteTypes = self._findNoteTypesForRow(r+repSkip)
            # The following assumes that there are as many entries in noteTypes
            # as there are vertical lines in the bar.
            c = self._findVerticalLine(startRow=r+repSkip)
            while c < len(tab[r+repSkip]):
                # Determine how many times this bar is repeated
                if repSkip:
                    repetitions = self._calculateBarRepetitions(r, c)
                else:
                    repetitions = 1
                for _ in xrange(repetitions):
                    for t in xrange(1, self.divisionsInBar + 1): # For every time in this bar
                        for d in xrange(0, len(noteTypes)): # For every drum in this bar
                            hitType = tab[r + d + repSkip][c + t]
                            if hitType == '-':
                                continue
                            elif hitType == 'o' or hitType == 'x':
                                pitch = self._noteNameToNoteNumberMap[noteTypes[d]]
                                volume = self._strikeVolume
                                m.addNote(track, channel, pitch, time, duration, volume)
                            elif hitType == 'O':
                                pitch = self._noteNameToNoteNumberMap[noteTypes[d]]
                                volume = self._accentVolume
                                m.addNote(track, channel, pitch, time, duration, volume)
                            elif hitType == 'g':
                                pitch = self._noteNameToNoteNumberMap[noteTypes[d]]
                                volume = self._ghostNoteVolume
                                m.addNote(track, channel, pitch, time, duration, volume)
                            elif hitType == 'r':
                                pitch = GMSpecDrumNameToMidiNote['Sticks']
                                volume = self._strikeVolume
                                m.addNote(track, channel, pitch, time, duration, volume)
                        time += duration
                # Check if there are more bars
                nextLineColumn = c + self.divisionsInBar + 1
                if self._isVerticalLine(nextLineColumn, r+repSkip) and nextLineColumn < len(tab[r+repSkip]) - 1:
                    c = nextLineColumn
                else:
                    break
        m.writeFile(file)


    def _calculateBarRows(self):
        """
        Calculates which rows of the tab text are the top rows of bars.
        """
        # For now, simply check whether the row contains a vertical line
        # character and is preceeded by a row that doesn't.
        tab = self._tab
        barRows = []
        r = 0
        while r < len(tab):
            if '|' in tab[r]:
                barRows.append(r)
                while r < len(tab) and '|' in tab[r]:
                    r += 1
            else:
                r += 1
        return barRows


    def _findAllNoteTypes(self):
        """
        Returns the set of note types.
        """
        types = set()
        for r in self._barRows:
            types.update(self._findNoteTypesForRow(r))
        return types


    def _findNoteTypesForRow(self, row):
        """
        Returns an ordered list of the note types corresponding to the bar
        whose top row is the given row.
        """
        tab = self._tab
        types = []
        while row < len(tab) and '|' in tab[row]:
            noteType = self._findNoteType(row)
            if noteType:
                types.append(noteType)
            row += 1
        return types


    def _findNoteType(self, row):
        """
        Finds the note type for a given row.
        """
        tab = self._tab
        noteType, sep, notes = tab[row].partition('|')
        return noteType.strip().rstrip(':-')


    def _findVerticalLine(self, startColumn=0, startRow=0):
        """
        Returns the first column on or after startColumn that is a vertical line /
        bar division.  If no column is found, returns None.
        """
        tab = self._tab
        for c in xrange(startColumn, len(tab[startRow])):
            if self._isVerticalLine(c, startRow):
                return c
        return None


    def _isVerticalLine(self, column, startRow):
        """
        Returns True if the column contains an unbroken vertical line starting
        from the startRow.
        """
        tab = self._tab
        if tab[startRow][column] == '|':
            for r in xrange(startRow, len(tab)):
                if column >= len(tab[r]) or tab[r].strip() == "" or tab[r][column] == " ":
                    break
                if tab[r][column] != '|':
                    return False
            return True
        else:
            return False


    def _calculateDivisionsInBar(self, row):
        """
        Returns the number of divisions in the bar whose top row is the given row.
        """
        start = self._findVerticalLine(0, row)
        if not start:
            raise TabParsingException("Could not find starting vertical bar.", 0, row)
        end = self._findVerticalLine(start + 1, row)
        if not end:
            raise TabParsingException("Could not find end vertical bar.", start + 1, row)
        return end - start - 1


    def _calculateBarRepetitions(self, row, column):
        """
        Determines how many times the current bar is played.
        """
        tab = self._tab
        # TODO: handle the case where this row at this column is padded out
        # with whitespace or is shorter than the rows below it.
        thisBar = tab[row][column+1:column+self.divisionsInBar+1].strip('- ' + string.ascii_letters)
        if thisBar:
            return int(thisBar)
        else:
            return 1


# todo: automatic time signature determination

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
    s = open("test.txt").read()
    t = Tab(s)
    t.writeMIDIFile(open("output.mid", "wb"))
