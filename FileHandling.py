import lzma
import bz2
import pathlib
import tempfile
import hashlib
import os


def create_archive(file: str, output: str, max_size: int = 20,
                   compress_whole: bool = True, compress_chunks: bool = True):
    max_target_size: int = max_size * 1024 * 1024
    with tempfile.TemporaryFile() as temporary:
        with open(file, "rb") as f:
            file_data = f.read()

            if compress_whole:
                temporary.write(bz2.compress(
                    os.path.basename(file).encode() + b'_.COM.!' + hashlib.sha1(file_data).hexdigest().encode() + b'_.COM.!'
                    + file_data, 9))
            else:
                temporary.write(
                    os.path.basename(file).encode() + b'_.COM.!' + hashlib.sha1(
                        file_data).hexdigest().encode() + b'_.COM.!'
                    + file_data)

        temporary.seek(0)
        chunk_counter = 0
        while chunk := temporary.read(max_target_size):
            compressed_chunk: bytes = lzma.compress(chunk, lzma.FORMAT_XZ) if compress_chunks else chunk
            with open(
                    f"{output}\\{
                    hashlib.sha1(file.encode()).hexdigest()[:6]
                    }{
                    chunk_counter.__str__().rjust(4, "0")
                    }{hashlib.sha1(chunk).hexdigest()[:6:]}.bin.xz.part", 'wb') as cf2:
                cf2.write(compressed_chunk)
            chunk_counter += 1


def dearchive(directory: str, compress_whole: bool = True, compress_chunks: bool = True):
    files = os.listdir(directory)
    compatible_files = {}
    for file in files:
        if file.endswith('.bin.xz.part'):
            id = file[:6]
            num = file[6:10]
            if id not in compatible_files:
                compatible_files[id] = {}
            compatible_files[id][num] = file

    for file_key, _ in compatible_files.items():
        working_file = compatible_files[file_key]

        with tempfile.TemporaryFile() as w:
            for i in range(len(working_file.keys())):
                file = working_file[str(i).rjust(4, "0")]

                with open(directory + '\\' + file, 'rb') as f:
                    w.write(lzma.decompress(f.read()) if compress_chunks else f.read())

            w.seek(0)

            reconstructed_data = bz2.decompress(w.read()) if compress_whole else w.read()
            file_name = reconstructed_data.split(b'_.COM.!')[0]
            saved_hash = reconstructed_data.split(b'_.COM.!')[1]
            reconstructed_data = reconstructed_data.split(b'_.COM.!', 2)[2]
            if hashlib.sha1(reconstructed_data).hexdigest() == saved_hash.decode():
                with open(directory + '\\' + file_name.decode(), 'wb') as wnf:
                    wnf.write(reconstructed_data)

                    for i in range(len(working_file.keys())):
                        file = working_file[str(i).rjust(4, "0")]
                        os.remove(directory + '\\' + file)
                    print(f'Successfully reconstructed file {directory + '\\' + file_name.decode()}')
            else:
                print('Reconstructed file hash does not match with the saved hash! Reconstruction halted!')
