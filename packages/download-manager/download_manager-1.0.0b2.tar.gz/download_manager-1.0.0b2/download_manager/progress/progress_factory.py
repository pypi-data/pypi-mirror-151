import functools
from .tdqm_progress_manager import TdqmProgressManager

progresses = {}


def progress_chunk_handling(func):
    @functools.wraps(func)
    def wrapper_chunk_download(*args, **kwargs):
        filename = kwargs.get('filename')
        size = kwargs.get('size')
        start = kwargs.get('start')
        stop = kwargs.get('stop')
        quiet = kwargs.get('quiet')
        if not quiet:
            append_progress(name=filename, total=size)

        try:
            value = func(*args, **kwargs)  # process transfer
        except Exception as e:
            raise e
        if not quiet:
            update_progress(name=filename, inc=stop-start)
            bar = get_progress_manager(name=filename, total=size)
            if bar._tqdm.n == size:
                bar._tqdm.close()
                remove_progress(name=filename)
        return value
    return wrapper_chunk_download


def get_progress_manager(name: str, total: int):
    global progresses
    if name in progresses.keys():
        return progresses[name]
    return TdqmProgressManager(name=name,
                               total=total,
                               unit="Bytes",
                               colour="GREEN"
                               )


def append_progress(name: str, total: int):
    global progresses
    progresses[name] = get_progress_manager(name, total)


def remove_progress(name: str):
    global progresses
    del progresses[name]


def update_progress(name: str, inc: int):
    global progresses
    progresses[name].update(inc)
