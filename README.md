`tabtomidi` is a library for generating
[MIDI](http://en.wikipedia.org/wiki/Musical_Instrument_Digital_Interface) files
from [ASCII drum tablature](http://en.wikipedia.org/wiki/ASCII_tab).  It powers
[tabtomidi.appspot.com](http://tabtomidi.appspot.com/).

The library is a work in progress.  There is limited to no support for:

- nested repetitions
- flams (they are treated as regular strikes)

Also, the library assumes that

- the tempo is constant throughout the song
- bars are marked by columns of pipe characters ('|')
- silence is indicated by dashes ('-')
- all bars are in the same time signature
- all bars have the same number of subdivisions

[![Build Status](https://travis-ci.org/JoshRosen/tabtomidi.png)](https://travis-ci.org/JoshRosen/tabtomidi)
