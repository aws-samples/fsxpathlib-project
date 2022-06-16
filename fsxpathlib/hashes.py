# -*- coding: utf-8 -*-


import hashlib

DEFAULT_CHUNK_SIZE = 1 << 13


def get_hash(
    file_obj,
    open_kwargs: dict = None,
    hash_meth=hashlib.md5,
    nbytes=0,
    chunk_size=DEFAULT_CHUNK_SIZE,
):
    if open_kwargs is None:
        open_kwargs = dict()
    if nbytes < 0:
        raise ValueError("chunk_size cannot smaller than 0")
    if chunk_size < 1:
        raise ValueError("chunk_size cannot smaller than 1")
    if (nbytes > 0) and (nbytes < chunk_size):
        chunk_size = nbytes
    m = hash_meth()
    with file_obj.open("rb", **open_kwargs) as f:
        if nbytes:  # use first n bytes
            have_reads = 0
            while True:
                have_reads += chunk_size
                if have_reads > nbytes:
                    n = nbytes - (have_reads - chunk_size)
                    if n:
                        data = f.read(n)
                        m.update(data)
                    break
                else:
                    data = f.read(chunk_size)
                    m.update(data)
        else:  # use entire content
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                m.update(data)

    return m.hexdigest()
