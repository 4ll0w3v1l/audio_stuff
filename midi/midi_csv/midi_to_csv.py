"""
This is the midi to csvs module.
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


def main(filename, output_dir):

    if not output_dir:
        output_dir = filename + "-output-csvs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # print("Outputting csvs files in to " + output_dir_name)

    # print("Processing " + filename + " in to " + filename[:-4] + ".csvs")
    assert filename.endswith(".mid"), "files must be midi files"
    mf = music21.midi.MidiFile()
    mf.open(filename)
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

    df.to_csv(output_dir + filename.split('/')[-1][:-4] + ".csvs")

    # print("Done creating csvs!")
