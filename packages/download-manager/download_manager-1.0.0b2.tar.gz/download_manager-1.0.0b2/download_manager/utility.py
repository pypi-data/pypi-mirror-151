import os
from _csv import reader
from dataclasses import dataclass
from math import ceil


@dataclass
class Chunk:
    start: int
    end: int


def slice_file(file_size: int, chunk_size=4194304):
    """
    Slices file as a list of ranges. Ranges are computed from the size of the
    file divide by the chunk size. A chunk is a minimum piece of the file to
    be transferred.

    The chunk size is default 4Mb and can be modified. Some bench shows that
    too small chunks reduces the transfer performances (could depend on the
    network MTU). Too big also could raise problem because of the memory
    usage.

    Parameters:
        file_size: (int) the file size to be transferred in byte.
        chunk_size: (int) the minimum chunk size in bytes (default 4194304).


    Return:
        A list of offset position chnuks in the input data to be transfer
        ([begin offset, end offset] in byte).
    """
    if not file_size:
        raise ValueError("Size of file is required.")

    chunk_list = []
    chunk_number = ceil(file_size / chunk_size)
    for chunk_count in range(chunk_number):
        start = chunk_count * chunk_size
        end = start + chunk_size - 1
        end = end if file_size > end else file_size - 1
        chunk_list.append(Chunk(start=start, end=end))

    return chunk_list


def check_file(output: str, name: str):
    """
        When the resume option is used, this
        method check if a file matching the pattern,
        of a download already started by the
        download manager is present (name+'.'+uuid).

        Parameters:
            output: (str) folder output.
            name: (str) The name of the file to search.


        Return:
            A tuple with a boolean and the name of the file when found.
        """
    output = '.' if output == '' else output
    for f in os.listdir(output):
        if f.startswith(name + '.'):
            return True, f
    return False, None


def parse_csv(path: str):
    with open(path, 'r') as read_obj:
        return [row[0] for row in reader(read_obj)]
