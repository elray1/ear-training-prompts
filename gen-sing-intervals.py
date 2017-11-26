from mingus.containers import Note
from mingus.containers import Bar
from mingus.midi import midi_file_out
from subprocess import call
import os

## major 3rds
base_notes = ["A", "B", "C", "D", "E", "F", "G"]
intervals =      [1,      2,      3,      4,      5,   6,         7,   8,      9,      10,     11,     12]
interval_names = ["min2", "maj2", "min3", "maj3", "4", "tritone", "5", "min6", "maj6", "min7", "maj7", "octave"]
interval_directions = ["up", "down"]

basen = Note(base_notes[0], 3)
baseb = Bar()
baseb.set_meter((1,4))
baseb.place_notes(basen, 4)
midi_file_out.write_Bar("base_note.mid", baseb, 100, 0)

intervaln = Note()
intervaln.from_int(int(basen) + intervals[3])
intervalb = Bar()
intervalb.set_meter((2,4))
intervalb.place_notes(intervaln, 4)
midi_file_out.write_Bar("interval_note.mid", intervalb, 100, 0)

os.system("timidity --output-24bit -A120 base_note.mid -Ow -o base_note.wav")
os.system("sox base_note.wav base_note_short.wav trim 0 4")
os.system("timidity --output-24bit -A120 interval_note.mid -Ow -o interval_note.wav")
os.system("sox interval_note.wav interval_note_short.wav trim 0 4")
os.system("sox base_note_short.wav instructions/sing_up_maj3.wav interval_note_short.wav combined.wav")
os.system("lame -a --tt 'Sing up maj3 from A' --tl 'Ear Training Prompts' --ta 'Evan Ray' -b 96 combined.wav sing-intervals/sing_up_maj3_from_A.mp3")
