import os
import pytest
import time
from tracemoepy import TraceMoe
from tracemoepy.errors import InvalidToken, ServerError, InvalidPath
from tracemoepy.helpers.constants import IMAGE_PREVIEW

from attrify import Attrify

tracemoe = TraceMoe()


def test_search():
    assert os.path.exists("flipped-good.webp")

    result = tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    assert isinstance(result, Attrify)
    time.sleep(1)
    result = tracemoe.search("flipped-good.webp", upload_file=True)
    assert isinstance(result, Attrify)
    

def test_b_natural_preview():
    result = tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)

    content = tracemoe.natural_preview(result)

    assert isinstance(content, bytes)
    time.sleep(1)
    preview = result.result[0].save("natural-preview.mp4")

    assert preview == True
    assert os.path.exists("natural-preview.mp4") == True
    time.sleep(1)
    preview = result.result[0].save("natural-preview-silent.mp4", mute=True)

    assert preview == True
    assert os.path.exists("natural-preview-silent.mp4") == True


def test_c_image_preview():

    result = tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    time.sleep(1)
    content = tracemoe.image_preview(result)
    assert isinstance(content, bytes)

    preview = result.result[0].save(
        save_path="image-preview.png", preview_type="image"
    )
    assert preview == True
    assert os.path.exists("image-preview.png") == True


def test_d_errors():
    tracemoe = TraceMoe()

    with pytest.raises(ServerError):
        tracemoe.search("https://example.com")

    result = tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    time.sleep(1)
    with pytest.raises(InvalidPath):
        result.result[0].save("preview.mp4", preview_type="/non-existant-type")
