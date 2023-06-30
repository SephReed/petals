import os
import pytest
import shutil

from huggingface_hub import snapshot_download

from petals.utils.peft import check_peft_repository, load_peft


NOSAFE_PEFT_REPO = "timdettmers/guanaco-7b"
SAFE_PEFT_REPO = "artek0chumak/guanaco-7b"
TMP_CACHE_DIR = "tmp_cache/"


def clear_dir(path_to_dir):
    shutil.rmtree(path_to_dir)
    os.mkdir(path_to_dir)


def dir_empty(path_to_dir):
    files = os.listdir(path_to_dir)
    return len(files) == 0


@pytest.mark.forked
def test_check_peft():
    assert not check_peft_repository(NOSAFE_PEFT_REPO), "NOSAFE_PEFT_REPO is safe to load."
    assert check_peft_repository(SAFE_PEFT_REPO), "SAFE_PEFT_REPO is not safe to load."


@pytest.mark.forked
def test_load_noncached(tmpdir):
    clear_dir(tmpdir)
    with pytest.raises(Exception):
        load_peft(NOSAFE_PEFT_REPO, cache_dir=tmpdir)
        
    assert dir_empty(tmpdir), "NOSAFE_PEFT_REPO is loaded"

    load_peft(SAFE_PEFT_REPO, cache_dir=tmpdir)

    assert not dir_empty(tmpdir), "SAFE_PEFT_REPO is not loaded"


@pytest.mark.forked
def test_load_cached(tmpdir):
    clear_dir(tmpdir)
    snapshot_download(SAFE_PEFT_REPO, cache_dir=tmpdir)
    
    load_peft(SAFE_PEFT_REPO, cache_dir=tmpdir)