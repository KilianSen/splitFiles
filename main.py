import argparse
import os
import sys
from FileHandling import create_archive, dearchive


def process_files(mode, input_path: str, output_path: str = None, max_size: int = None,
                  compress_whole: bool = True, compress_chunks: bool = True):
    """
    Process files based on the mode of operation
    :param mode: Defines the type of operation to perform: archive, dearchive, auto
    :param input_path: Path to file to archive or directory to dearchive
    :param output_path: Path where to save the archive
    :param max_size: Max chunk size in megabytes
    :param compress_whole: Enable compression of the whole file before the archival.
    This value has to be the same for dearchiving.
    :param compress_chunks:Enable compression of the chunk files during archival.
    This value has to be the same for dearchiving.
    """
    if not os.path.exists(input_path):
        raise ValueError(f'Input path {input_path} does not exist')

    if mode == 'auto':
        mode = 'archive' if os.path.isfile(input_path) else 'dearchive'

    if output_path and not os.path.isdir(os.path.dirname(output_path)):
        raise ValueError(f'Output path {output_path} directory does not exist')

    if mode == 'archive':
        if not output_path or not max_size:
            raise ValueError('For "archive" mode, both "output_path" and "max_size" parameters are required')
        create_archive(input_path, output_path, max_size, compress_whole, compress_chunks)
    elif mode == 'dearchive':
        dearchive(input_path, compress_whole, compress_chunks)
    else:
        raise ValueError('Invalid mode!')


def main():
    parser = argparse.ArgumentParser(description='Process some parameters.')

    parser.add_argument('-m', '--mode', type=str, default='auto',
                        help='Defines the type of operation to perform: archive, dearchive, auto')
    parser.add_argument('-i', '--input_path', type=str, required=True,
                        help='Path to file to archive or directory to dearchive')
    parser.add_argument('-o', '--output_path', type=str, default=None,
                        help='Path where to save the archive')
    parser.add_argument('-s', '--max_size', type=int, default=15,
                        help='Max chunk size in whole megabytes')

    parser.add_argument('-c1', '--compress_whole', type=bool, default=True,
                        help='Enable compression of the whole file before the archival.'
                             'This value has to be the same for dearchiving.')
    parser.add_argument('-c2', '--compress_chunk', type=bool, default=True,
                        help='Enable compression of the chunk files during archival.'
                             'This value has to be the same for dearchiving.')

    args = parser.parse_args()

    try:
        process_files(args.mode, args.input_path, args.output_path, args.max_size,
                      args.compress_whole, args.compress_chunk)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
