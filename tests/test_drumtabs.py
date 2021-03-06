import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.dirname(__file__))
import codecs
import py.test
import filecmp
from tabtomidi import Tab, TabParsingException, UnmappableNoteNamesException

output_verification_tests = [
    ('simple_4_4_beat',     {'tab' : 'testdata/simple_4_4_beat.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('repetition_4x',       {'tab' : 'testdata/repetition_4x.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('repetition_4x_unders',{'tab' : 'testdata/repetition_4x_underscore.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('repetition_4x_equals',{'tab' : 'testdata/repetition_4x_equals.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('repetition_2x_2x',    {'tab' : 'testdata/repetition_2x_2x.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('repetition_1x_2x_1x', {'tab' : 'testdata/repetition_1x_2x_1x.txt',
                             'expected_midi' : 'testdata/repetition_4x.mid'}),
    ('unknown_strike_types',{'tab' : 'testdata/unknown_strike_types.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('variable_bar_lengths',{'tab' : 'testdata/variable_bar_lengths.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('two_bar_repetition',  {'tab' : 'testdata/two_bar_repetition.txt',
                             'expected_midi' : 'testdata/two_bar_repetition.mid'}),
    ('no_initial_pipe',     {'tab': 'testdata/simple_4_4_beat_no_initial_pipe.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('odd_pipe_chars',      {'tab': 'testdata/simple_4_4_beat_odd_pipe_chars.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
    ('trailing text',       {'tab': 'testdata/simple_4_4_beat_trailing_text.txt',
                             'expected_midi' : 'testdata/simple_4_4_beat.mid'}),
]


def test_string_without_tab():
    with py.test.raises(TabParsingException):
        Tab("")
    with py.test.raises(TabParsingException):
        Tab("""
        This text contains no bar rows.
        An custom exception should be thrown
        if we try to generate a tab from this.
        """)


def test_unknown_strike_types_are_identified():
    tab = Tab(file('testdata/unknown_strike_types.txt').read())
    assert tab.unknown_strike_types == set(['Q', 'S', 'X', 'Z', 'z'])


def test_walk_notes_works_with_unknown_note_types():
    # This should not throw an exception.
    tab = Tab(file('testdata/simple_4_4_beat.txt').read(),
              note_name_to_number_map = {})
    with py.test.raises(UnmappableNoteNamesException):
        tab.write_midi_file(open(os.devnull, 'w'))


def pytest_generate_tests(metafunc):
    if metafunc.function == test_generated_midi_matches_expected_midi:
        for test in output_verification_tests:
            metafunc.addcall(id=test[0], funcargs=test[1])


def test_generated_midi_matches_expected_midi(tmpdir, tab, expected_midi):
    actual_midi = tmpdir.join("actual.mid").strpath

    tab = Tab(codecs.open(tab, "r", "utf-8").read())
    tab.write_midi_file(open(actual_midi, "wb"))
    assert filecmp.cmp(actual_midi, expected_midi)
