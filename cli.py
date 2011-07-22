"""
A command-line tool for testing the tabtomidi library.
"""
import argparse

from drumtabs import Tab
from collections import defaultdict

def main():
    """
    Main method of the command line interface
    """
    parser = argparse.ArgumentParser(
        description="Convert drum tabs to midi files.")
    parser.add_argument("tab_file", type=argparse.FileType('r'))
    parser.add_argument("midi_output_file", type=argparse.FileType('w'))
    args = parser.parse_args()
    tab_text = args.tab_file.read()
    tab = Tab(tab_text, note_name_to_number_map=defaultdict(int))
    tab = Tab(tab_text)
    tab.write_midi_file(args.midi_output_file)


if __name__ == "__main__":
    main()
