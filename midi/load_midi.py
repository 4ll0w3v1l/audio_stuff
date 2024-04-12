import concurrent.futures
from midi_csv.midi_to_csv import main
import os, time


def discover_folders(folder):
    import os
    for d in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, d)):
            yield from discover_folders(os.path.join(folder, d))

        if os.path.isfile(os.path.join(folder, d)):
            yield os.path.join(folder, d)


if __name__ == '__main__':
    # TODO: Add non-constant paths
    files = set([x for x in discover_folders('/Users/3vil/audio/audio_stuff/data/midi/')])
    output = '/Users/3vil/audio/audio_stuff/data/csvs/'
    workers = 16

    print(f'FILES DISCOVERED: {len(files)}')

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        #  TODO: Speed up andrewchenk's script
        futures = [executor.submit(main, file, output) for file in files]
        results = []
        counter = 0
        prev_time = time.time()
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            counter += 1
            print(f'{(len(results) / len(files)) * 100}% complete')
            print(f'ETA: {((time.time() - prev_time) * (len(files) / counter - 1)) * 60 } minutes')
            prev_time = time.time()
