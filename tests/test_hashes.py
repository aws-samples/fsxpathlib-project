# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from fsxpathlib.hashes import get_hash


def test_get_hash():
    p = Path(__file__)
    assert get_hash(p, nbytes=999999) == get_hash(p)
    assert get_hash(p, nbytes=256) != get_hash(p)

    with pytest.raises(ValueError):
        get_hash(p, nbytes=-1)

    with pytest.raises(ValueError):
        get_hash(p, chunk_size=0)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
