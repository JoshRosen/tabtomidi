import string
import re
from midiutil.MidiFile import MIDIFile
from tabtomidi.notenames import DEFAULT_NOTE_NAME_TO_NUMBER_MAP, \
    GM_SPEC_NOTE_NAME_TO_NUMBER_MAP


class TabParsingException(Exception):
    """Base class for all exceptions due to unparsable tabs."""

    def __init__(self, message, row=None, column=None):
        Exception.__init__(self, message)
        self.row = row
        self.column = column


class UnmappableNoteNamesException(TabParsingException):
    """
    Raised when the parser cannot map one or more note names to midi notes.
    The note_names attribute provides the set of unmappable note names.
    """

    def __init__(self, note_names):
        TabParsingException.__init__(self,
            "Some note names could not be mapped to midi notes: " + str(note_names))
        self.note_names = note_names


class Tab(object):
    """
    Provides information about drum tabs and generates midi files from them.
    """

    def __init__(self, tabtext,
                 note_name_to_number_map=None,
                 bpm=100, strike_volume=70, accent_volume=110,
                 ghost_note_volume=50):
        """Constructs a Tab object from a string representing a tab."""
        # Replace pipe character loookalikes with proper pipe characters
        # See http://stackoverflow.com/questions/10572627/
        pipe_lookalikes = u'\u007c\u00a6\u2758\uffc5\uffe4'
        for lookalike in pipe_lookalikes:
            tabtext = tabtext.replace(lookalike, '|')
        self._tab = [l.rstrip() for l in tabtext.splitlines()]
        self._bpm = bpm
        self._strike_volume = strike_volume
        self._accent_volume = accent_volume
        self._ghost_note_volume = ghost_note_volume
        # perform pre-processing to remove count rows:
        for r in range(len(self._tab)):
            if self._is_count_row(r):
                self._tab[r] = ""
        self._bar_rows = self._calculate_bar_rows()
        if not self._bar_rows:
            raise TabParsingException("Could not find any bars in input text.")
        self._note_types = None
        self._strike_types = None
        if note_name_to_number_map == None:
            self.note_name_to_number_map = DEFAULT_NOTE_NAME_TO_NUMBER_MAP
        else:
            self.note_name_to_number_map = note_name_to_number_map
        # Assuming that all columns notes have the same duration, i.e. each
        # column represents a 16th note.
        # Some tabs have extra characters between the bars, i.e. 33 instead of
        # 32, so simply counting the number of characters between the bars will
        # not always work.
        # For now, use the number of divisions in the first bar to calculate
        # the note duration.  This should probably be changed to find the mode
        # of the set of divisions in each bar.
        self.divisions_in_bar = self._calculate_divisions_in_bar(
            self._bar_rows[0])

    # TODO: add indirect accessors and setters before allowing this class to be
    # subclassed.
    def __set_note_name_to_number_map(self, note_name_to_number_map):
        """Setter for note_name_to_number_map property."""
        self.__note_name_to_number_map = \
            dict((note, note_name_to_number_map[note]) for note in
            note_name_to_number_map.keys() if note in self.note_types)

    def __get_note_name_to_number_map(self):
        """Accessor for note_name_to_number_map property."""
        return self.__note_name_to_number_map

    note_name_to_number_map = property(
        __get_note_name_to_number_map, __set_note_name_to_number_map,
        doc="""Get or set the note name to note number map.""")

    @property
    def note_types(self):
        """The set of all note types."""
        if self._note_types == None:
            self._note_types = self._find_all_note_types()
        return self._note_types

    @property
    def strike_types(self):
        """The set of all strike types."""
        if self._strike_types == None:
            self._strike_types = self._find_all_strike_types()
        return self._strike_types

    @property
    def strike_type_volume_map(self):
        return {
            'O' : self._accent_volume,
            'g' : self._ghost_note_volume,
            'r' : self._strike_volume,
            'o' : self._strike_volume,
        }

    @property
    def unknown_strike_types(self):
        """The set of strike types without defined handling behavior."""
        return self.strike_types.difference(
            set(self.strike_type_volume_map.keys()))

    def _volume_for_strke_type(self, strike_type):
        """
        Given a character representing a type of strike, determine how loud the
        note should be played.
        """
        if strike_type in self.strike_type_volume_map.keys():
            return self.strike_type_volume_map[strike_type]
        else:
            return self._strike_volume

    def write_midi_file(self, file_object):
        """Writes midi generated from this tab to the given file object."""
        # Throw an exception if there are note names for which we can't
        # determine the proper note numbers.
        unmappable_note_names = self.note_types.difference(
            self.note_name_to_number_map.keys())
        if unmappable_note_names:
            raise UnmappableNoteNamesException(unmappable_note_names)

        midifile = MIDIFile(1)
        track = 0
        channel = 9
        duration = round(4.0 / self.divisions_in_bar, 10)
        # 4.0 is because midiutil's  unit of time is the quarter note.
        midifile.addTrackName(track, 0, "")
        midifile.addTempo(track, 0, self._bpm)
        for note in self.walk_notes():
            strike_type = note['strike_type']
            volume = self._volume_for_strke_type(strike_type)
            if strike_type == 'r':
                pitch = GM_SPEC_NOTE_NAME_TO_NUMBER_MAP['Sticks']
            else:
                pitch = self.note_name_to_number_map[note['note_type']]
            midifile.addNote(track, channel, pitch, note['time'], duration,
                             volume)
        midifile.writeFile(file_object)

    def walk_notes(self, ignore_repetition=False):
        """A generator that yields each note in order."""
        tab = self._tab
        time = 0.0
        duration = round(4.0 / self.divisions_in_bar, 10)
        # 4.0 is because midiutil's  unit of time is the quarter note.

        for r in self._bar_rows:
            # Determine whether the first row contains notes or repetition
            # information.
            if self._contains_repetitions(r):
                has_repetitions = True
                repetition_info = r
                r += 1
            else:
                has_repetitions = False
            r = self._find_first_note_row_for_bar(r)
            # Determine which drums are present in this group of bars.
            note_types = self._find_note_types_for_row(r)
            # The following assumes that there are as many entries in
            # note_types as there are vertical lines in the bar.
            c = self._find_vertical_line(start_row=r)
            # Support bars that leave out the leftmost pipe character.
            if c - (self.divisions_in_bar + 1) > 0:
                c -= (self.divisions_in_bar + 1)
            while c < len(tab[r]) - 1:
                if has_repetitions and not ignore_repetition:
                    # Determine the length of the repeated section.
                    num_cols_to_parse = len(tab[repetition_info][c+1:].split('|', 1)[0])
                    if num_cols_to_parse == 0:
                        num_cols_to_parse = self._find_vertical_line(c+1, r) - c - 1
                    # Determine how many times the section is repeated.
                    repetitions = self._calculate_repetitions(repetition_info, c)
                else:
                    num_cols_to_parse = self._find_vertical_line(c+1, r) - c - 1
                    repetitions = 1
                for _ in xrange(repetitions):
                    for t in xrange(1, num_cols_to_parse+1):
                        # For every time in this bar or repeated section:
                        if not self._is_vertical_line(c+t, r):
                            for d in xrange(0, len(note_types)):
                                # For every drum in this bar:
                                if c + t >= len(tab[r + d]) and \
                                    tab[r + d].strip()[-1] == '|':
                                    # This is to handle cases where the last
                                    # row of a group of bars has fewer columns
                                    continue
                                strike_type = tab[r + d][c + t]
                                if strike_type in '-|':
                                    continue
                                else:
                                    yield { 'strike_type' : strike_type,
                                            'note_type' : note_types[d],
                                            'time' : time, }
                            time += duration
                c += num_cols_to_parse + 1
                if not self._is_vertical_line(c, r):
                    break

    def _calculate_bar_rows(self):
        """Calculates which rows of the tab text are the top rows of bars."""
        tab = self._tab
        bar_rows = []
        row = 0
        while row < len(tab):
            if '|' in tab[row]:
                bar_rows.append(row)
                while row < len(tab) and ('|' in tab[row] or
                    self._contains_triplets(row)):
                    row += 1
            else:
                row += 1
        return bar_rows

    def _find_first_note_row_for_bar(self, row):
        """
        Find the first row of the bar starting on or after the given row that
        contains notes (as opposed to repetition information, comments, or
        triplet marks.
        """
        r = row
        while r < len(self._tab) and (self._contains_repetitions(r) or \
            self._contains_triplets(r)):
            r += 1
        if r >= len(self._tab) or not self._find_vertical_line(start_row=r):
            raise TabParsingException("Bar without notes")
        return r

    def _find_all_note_types(self):
        """Returns the set of note types."""
        types = set()
        for row in self._bar_rows:
            note_row = self._find_first_note_row_for_bar(row)
            types.update(self._find_note_types_for_row(note_row))
        return types

    def _find_note_types_for_row(self, row):
        """
        Returns an ordered list of the note types corresponding to the bar
        whose top note row is the given row.
        """
        tab = self._tab
        types = []
        while row < len(tab) and '|' in tab[row]:
            if not self._contains_repetitions(row):
                note_type = self._find_note_type(row)
                if note_type:
                    types.append(note_type)
            row += 1
        return types

    def _find_note_type(self, row):
        """Finds the note type for a given row."""
        tab = self._tab
        note_type = tab[row].partition('|')[0]
        note_type = note_type.strip().split(' ')[0]
        return note_type.rstrip(' :-')

    def _find_all_strike_types(self):
        """Returns the set of strike types."""
        types = set()
        for note in self.walk_notes(ignore_repetition=True):
            types.update(note['strike_type'])
        return types

    def _find_vertical_line(self, start_column=0, start_row=0):
        """
        Returns the first column on or after start_column that is a vertical
        line / bar division.  If no column is found, returns None.
        """
        tab = self._tab
        for column in xrange(start_column, len(tab[start_row])):
            if self._is_vertical_line(column, start_row):
                return column
        return None

    def _is_vertical_line(self, column, start_row):
        """
        Returns True if the column contains an unbroken vertical line
        starting from the start_row."""
        tab = self._tab
        if tab[start_row][column] == '|':
            for row in xrange(start_row, len(tab)):
                if column >= len(tab[row]) \
                   or tab[row].strip() == "" \
                   or tab[row][column] == " ":
                    break
                if tab[row][column] != '|':
                    return False
            return True
        else:
            return False

    def _calculate_divisions_in_bar(self, row):
        """
        Returns the number of divisions in the bar whose top row is the
        given row.
        """
        # Find the first row that contains notes
        row = self._find_first_note_row_for_bar(row)
        # Count the number of characters between the vertical bars.
        start = self._find_vertical_line(0, row)
        if not start:
            raise TabParsingException("Could not find starting vertical bar.",
                                      0, row)
        end = self._find_vertical_line(start + 1, row)
        if not end:
            raise TabParsingException("Could not find end vertical bar.",
                                      start + 1, row)
        return end - start - 1

    def _calculate_repetitions(self, row, column):
        """
        Determines how many times the region whose start is at the given row
        and column is repeatd.  Assumes that the row contains repetition
        information (the row should not be the top row of notes).
        """
        tab = self._tab
        # TODO: handle the case where this row at this column is padded out
        # with whitespace or is shorter than the rows below it.
        fill_characters = '=-_ '
        repetition_count = tab[row][column+1:].split('|', 1)[0]
        repetition_count = repetition_count.strip(fill_characters +
                                                  string.ascii_letters)
        if repetition_count:
            try:
                reps = int(repetition_count)
                if reps == 1:
                    # "repeat 1x" probably means "play this section twice"
                    return 2
                else:
                    return reps
            except ValueError:
                # TODO: should probably log a warning here.
                return 1
        else:
            return 1

    def _contains_repetitions(self, row):
        """
        Return True if the row contains repetition information, False
        otherwise.
        """
        row_text = self._tab[row]
        if re.search(r"repeat|\|[-_=]*(\d+x|x\d+)[-_=]*\|", row_text):
            return True
        return not self._find_note_type(row)

    def _contains_triplets(self, row):
        """
        Return True if the row contains notation indicating triplets, False
        otherwise.
        """
        row_text = self._tab[row]
        if re.search(r"\(3\)", row_text):
            return True
        else:
            return False

    def _is_count_row(self, row):
        """
        Return True if the row contains notation indicating a count, False
        otherwise.  For example: | 1 e & a 2 e & a 3 e & a 4 e & a |
        """
        row_text = self._tab[row]
        if '&' in row_text or '+' in row_text:
            return True
        return False


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
