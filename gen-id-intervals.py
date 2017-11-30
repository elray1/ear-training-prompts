from mingus.containers import Note
from mingus.containers import Bar
from mingus.midi import midi_file_out
from subprocess import call
import os

base_notes = ["A", "B", "C", "D", "E", "F", "G"]
interval_values = [1,     2,      3,      4,      5,   6,         7,   8,      9,      10,     11,     12]
interval_names = ["min2", "maj2", "min3", "maj3", "4", "tritone", "5", "min6", "maj6", "min7", "maj7", "octave"]
interval_directions = ["down", "up"]

#base_notes = ["A"]
#interval_values = [4,     7,   10,     12]
#interval_names = ["maj3", "5", "min7", "octave"]
#interval_directions = ["down", "up"]

for base_note in base_notes:
    for interval_ind in range(0, 12):
        for direction_ind in range(0, 2):
            if interval_directions[direction_ind] == "down":
                base_octave = 4
            else:
                base_octave = 3
            if base_note == "G" or base_note == "A" or base_note == "B":
                base_octave -= 1
            basen = Note(base_note, base_octave)
            baseb = Bar()
            baseb.set_meter((1,4))
            baseb.place_notes(basen, 4)
            midi_file_out.write_Bar("base_note.mid", baseb, 100, 0)
            
            intervaln = Note()
            direction_sign = 2 * (direction_ind - 0.5)
            intervaln.from_int(int(int(basen) + direction_sign * (interval_values[interval_ind])))
            intervalb = Bar()
            intervalb.set_meter((2,4))
            intervalb.place_notes(intervaln, 4)
            midi_file_out.write_Bar("interval_note.mid", intervalb, 100, 0)
            
            os.system("timidity --output-24bit -A120 base_note.mid -Ow -o base_note.wav")
            os.system("timidity --output-24bit -A120 interval_note.mid -Ow -o interval_note.wav")
            os.system("sox base_note.wav base_note_short.wav trim 0 1.5")
            os.system("sox interval_note.wav interval_note_short.wav trim 0 4.5")
            os.system("sox instructions/" +
                interval_names[interval_ind] +
                ".wav instructions.wav trim 0 1.5")
            os.system("sox base_note_short.wav interval_note_short.wav instructions.wav combined.wav")
            os.system("lame -a --tt 'Id " +
                interval_directions[direction_ind] + " " +
                interval_names[interval_ind] + " from " +
                base_note +
                "' --tl 'Ear Training Prompts' --ta 'Evan Ray' -b 96 combined.wav id-intervals/id_" +
                interval_directions[direction_ind] + "_" +
                interval_names[interval_ind] + "_from_" +
                base_note +
                ".mp3")
