import difflib
import os
import py.test
from filecmp import cmp
from drumtabs import Tab, TabParsingException, UnmappableNoteNamesException

output_verification_tests = [
    ('simple_4_4_beat',     {'tab' : 'testdata/simple_4_4_beat.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('repetition_4x',       {'tab' : 'testdata/repetition_4x.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('repetition_2x_2x',    {'tab' : 'testdata/repetition_2x_2x.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('repetition_1x_2x_1x', {'tab' : 'testdata/repetition_1x_2x_1x.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('unknown_strike_types',{'tab' : 'testdata/unknown_strike_types.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('two_bar_repetition',  {'tab' : 'testdata/two_bar_repetition.txt',
                             'expected_midi' : 'testdata/two_bar_repetition.mid'}),
]


def test_string_without_tab():
    with py.test.raises(TabParsingException):
        t = Tab("")
    with py.test.raises(TabParsingException):
        t = Tab("""
        This text contains no bar rows.
        An custom exception should be thrown
        if we try to generate a tab from this.
        """)


def test_unknown_strike_types_are_identified():
    t = Tab(file('testdata/unknown_strike_types.txt').read())
    assert t._unknownStrikeTypes == set(['Q', 'S', 'X', 'Z', 'z'])


def test_walkNotes_works_with_unknown_note_types():
    # This should not throw an exception.
    t = Tab(file('testdata/simple_4_4_beat.txt').read(),
            noteNameToNoteNumberMap = {})
    with py.test.raises(UnmappableNoteNamesException):
        t.writeMIDIFile(open(os.devnull, 'w'))


def pytest_generate_tests(metafunc):
    if metafunc.function == test_generated_midi_matches_expected_midi:
        for test in output_verification_tests:
            metafunc.addcall(id=test[0], funcargs=test[1])


def test_generated_midi_matches_expected_midi(tmpdir, tab, expected_midi):
    actual_midi = tmpdir.join("actual.mid").strpath

    t = Tab(file(tab).read())
    t.writeMIDIFile(open(actual_midi, "wb"))
    assert cmp(actual_midi, expected_midi)
