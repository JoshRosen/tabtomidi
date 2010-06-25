import difflib
from filecmp import cmp
from drumtabs import Tab

def test_simple_4_4_beat(tmpdir):
    actual = tmpdir.join("simple_4_4_beat.mid").strpath
    expected = "testdata/simple_4_4_beat.mid"

    t = Tab(file("testdata/simple_4_4_beat.txt").read())
    assert t._BPM == 100

    t.writeMIDIFile(actual)
    assert cmp(actual, expected)
