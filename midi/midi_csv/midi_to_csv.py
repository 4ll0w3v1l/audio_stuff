"""
This is the midi to csv module. 
"""

# TODO: ADD CHANNEL SUPPORT
import os
import argparse

import music21
import pandas as pd


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def main(input_dir_name, output_dir_name):
    is_dir(input_dir_name)
    input_dir = os.fsencode(input_dir_name)
    output_dir_name = output_dir_name

    if not output_dir_name:
        output_dir_name = input_dir_name + "-output-csvs"

    if not os.path.exists(output_dir_name):
        os.makedirs(output_dir_name)

    # print("Outputting csv files in to " + output_dir_name)

    for file in os.listdir(input_dir):
        filename = os.fsdecode(file)
        # print("Processing " + filename + " in to " + filename[:-4] + ".csv")
        assert filename.endswith(".mid"), "files must be midi files"
        mf = music21.midi.MidiFile()
        mf.open(input_dir_name + "/" + filename)
        mf.read()
        mf.close()
        s = music21.midi.translate.midiFileToStream(
            mf,
            quantizePost=False).flatten()  # quantize is what rounds all note durations to real music note types, not needed for our application
        # Convert chords in to notes.
        # TODO: consider chords as separate objects from notes? Everything's in music21 anyways
        df = pd.DataFrame(columns=["note_name", "start_time", "duration", "velocity", "tempo"])
        for g in s.recurse().notes:
            if g.isChord:
                for pitch in g.pitches:
                    x = music21.note.Note(pitch, duration=g.duration)
                    x.volume.velocity = g.volume.velocity

                    x.offset = g.offset
                    s.insert(x)
        # ALERT: assumes only one tempo
        note_tempo = s.metronomeMarkBoundaries()[0][2].number
        for note in s.recurse().notes:
            if note.isNote:
                new_df = pd.DataFrame([[note.pitch, round(float(note.offset), 3), round(note.duration.quarterLength, 3),
                                        note.volume.velocity, note_tempo]],
                                      columns=["note_name", "start_time", "duration", "velocity", "tempo"])

                df = pd.concat([df, new_df], ignore_index=True)

        df.to_csv(output_dir_name + "/" + filename[:-4] + ".csv")

    # print("Done creating csvs!")
