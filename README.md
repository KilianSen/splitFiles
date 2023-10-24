# splitFiles

This application helps you to split a large file into an archive of multiple smaller files. 
It also allows you to reconstruct the original file from these smaller chunks.

It uses `bz2` and `lzma` compression algorithms for archiving and decompressing files respectively. 
It also adds a layer of validation by comparing hash of reconstructed and original file.

## Dependencies

- Python 3 (tested 3.10 and above)

## How to Run

1. Clone this repository to your local machine.
2. In your terminal, navigate to the directory where the files are located.
3. You can run the script by supplying command line arguments:
    - `-m` / `--mode` : Defines the type of operation to perform: archive, dearchive, auto
    - `-i` / `--input_path` : Path to file to archive or directory to dearchive
    - `-o` / `--output_path` : Path where to save the archive
    - `-s` / `--max_size` : Max chunk size in whole megabytes

For example:
```sh
python file_processing.py --mode archive --input_path "./input.txt" --output_path "./output" --max_size 20
```
### Executables
Found at
https://github.com/KilianSen/splitFiles/releases

## Features

- Split a file into multiple parts.
- The whole file is compressed using `bz2` and the parts are compressed using `lzma` algorithms. (Double compression is often not useful)
- Each file chunk gets a unique name, making it easy to keep track of files.
- Possibility to reconstructing the original file by putting the parts together in the correct order.
- Validation is performed by comparing hash of the reconstructed and original file.
