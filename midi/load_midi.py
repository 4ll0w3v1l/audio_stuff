import concurrent.futures
from midi_csv.midi_to_csv import main


def discover_folders(folder):
    import os
    for d in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, d)):
            yield from discover_folders(os.path.join(folder, d))

        if os.path.isfile(os.path.join(folder, d)):
            yield os.path.join(folder)


if __name__ == '__main__':
    # TODO: Add non-constant paths
    folders = set([x for x in discover_folders('/Users/3vil/audio/audio_stuff/data/midi/')])
    output = '/Users/3vil/audio/audio_stuff/csv_from_midi'
    workers = 4

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        #  TODO: Speed up andrewchenk's script
        futures = [executor.submit(main, folder, output) for folder in folders]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        for result in results:
            print(result.decode())

