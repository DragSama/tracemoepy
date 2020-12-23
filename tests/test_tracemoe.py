import os
import pytest

from tracemoepy import TraceMoe
from tracemoepy.errors import (
    InvalidToken,
    ServerError,
    InvalidPath
)
from tracemoepy.helpers.superdict import SuperDict
from tracemoepy.helpers.constants import IMAGE_PREVIEW

tracemoe = TraceMoe()

def test_search():

    result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
    assert isinstance(result, SuperDict)

    result = tracemoe.search('flipped-good.webp', upload_file = True)
    assert isinstance(result, SuperDict)
    # Not testing because tracemoe is having issues with base64 encoded images.
    #result = tracemoe.search('flipped-good.webp', encode = True)
    #assert isinstance(result, SuperDict)

def test_b_natural_preview():
    result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

    content = tracemoe.natural_preview(result)

    assert isinstance(content, bytes)

    preview = result.docs[0].save('natural-preview.mp4')

    assert preview == True
    assert os.path.exists('natural-preview.mp4') == True

    preview = result.docs[0].save('natural-preview-silent.mp4', mute = True)

    assert preview == True
    assert os.path.exists('natural-preview-silent.mp4') == True

def test_c_image_preview():

    result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

    content = tracemoe.image_preview(result)
    assert isinstance(content, bytes)

    preview = result.docs[0].save(save_path='image-preview.png', preview_path=IMAGE_PREVIEW)
    assert preview == True
    assert os.path.exists('image-preview.png') == True

def test_d_errors():
    tracemoe = TraceMoe(api_token = 'spfskjapofapokfapkf')

    with pytest.raises(InvalidToken):
        tracemoe.get_me()

    with pytest.raises(InvalidToken):
        tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

    tracemoe = TraceMoe()

    with pytest.raises(ServerError):
        tracemoe.search('https://example.com')

    result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

    with pytest.raises(InvalidPath):
        result.docs[0].save('preview.mp4', preview_path = '/non-existant-path')


if __name__ == '__main__':
    unittest.main()
