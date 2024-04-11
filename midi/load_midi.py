from mido import tempo2bpm, tick2second


def discover_folders(folder):
    import os
    for d in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, d)):
            yield from discover_folders(os.path.join(folder, d))

        if os.path.isfile(os.path.join(folder, d)):
            yield os.path.join(folder, d)


def load_from_folder(folder, max_files=None):
    from mido import MidiFile
    import os

    files = list(discover_folders(folder))
    if max_files:
        files = files[:max_files]

    for f in files:
        if os.path.isfile(f) and f.endswith('.mid'):
            yield MidiFile(f)


def get_notes_from_channel(file, channel=0):
    notes = []

    for msg in file:
        if msg.type == 'note_on' or msg.type == 'note_off':
            if msg.channel == channel:
                notes.append(msg)


def midi_to_np():
    import numpy as np
    files = load_from_folder('../../data/midi/', 1)

    for midi_file in files:
        print(midi_file.filename)
        print(midi_file.length)

        tempos = []
        num_denum = []

        for msg in midi_file:
            if msg.is_meta:
                print(msg)
            if msg.is_meta and msg.type == 'time_signature':
                num_denum.append(msg.numerator)
                num_denum.append(msg.denominator)
            if msg.is_meta and msg.type == 'set_tempo':
                tempos.append(msg.tempo)
        tempo = round(tempo2bpm(sum(tempos) / len(tempos), (num_denum[0], num_denum[1])))

        for msg in midi_file:
            print(msg)


midi_to_np()
