import difflib
from filecmp import cmp
from drumtabs import Tab

output_verification_tests = [
    ('simple_4_4_beat', {'tab' : 'testdata/simple_4_4_beat.txt',
                         'expected_midi' : 'testdata/simple_4_4_beat.mid'})
]

def pytest_generate_tests(metafunc):
    if metafunc.function == test_generated_midi_matches_expected_midi:
        for test in output_verification_tests:
            metafunc.addcall(id=test[0], funcargs=test[1])

def test_generated_midi_matches_expected_midi(tmpdir, tab, expected_midi):
    actual_midi = tmpdir.join("actual.mid").strpath

    t = Tab(file(tab).read())
    t.writeMIDIFile(open(actual_midi, "wb"))
    assert cmp(actual_midi, expected_midi)
