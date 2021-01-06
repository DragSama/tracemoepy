import os
import pytest
import aiohttp

from tracemoepy import AsyncTrace
from tracemoepy.errors import InvalidToken, ServerError, InvalidPath
from tracemoepy.helpers.constants import IMAGE_PREVIEW

from attrify import Attrify

pytestmark = pytest.mark.asyncio

assert os.path.exists("flipped-good.webp")

async def test_a_intializing():

    tracemoe = AsyncTrace()
    await tracemoe.aio_session.close()

    session = aiohttp.ClientSession()
    tracemoe = AsyncTrace(session=session)
    await tracemoe.aio_session.close()


async def test_b_search():
    assert os.path.exists("flipped-good.webp")

    tracemoe = AsyncTrace()

    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    assert isinstance(result, Attrify)

    # Don't ask why.
    # result = await tracemoe.search("flipped-good.webp", upload_file=True)
    # assert isinstance(result, Attrify)

    # Not testing because tracemoe is having issues with base64 encoded images.
    # result = tracemoe.search('flipped-good.webp', encode = True)
    # assert isinstance(result, Attrify)

    await tracemoe.aio_session.close()


async def test_c_natural_preview():
    tracemoe = AsyncTrace()

    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    content = await tracemoe.natural_preview(result)

    assert isinstance(content, bytes)

    preview = await result.docs[0].save("natural-preview.mp4")

    assert preview == True
    assert os.path.exists("natural-preview.mp4") == True

    preview = await result.docs[0].save("natural-preview-silent.mp4", mute=True)

    assert preview == True
    assert os.path.exists("natural-preview-silent.mp4") == True

    await tracemoe.aio_session.close()


async def test_d_image_preview():
    tracemoe = AsyncTrace()

    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)

    content = await tracemoe.image_preview(result)

    assert isinstance(content, bytes)

    preview = await result.docs[0].save(
        save_path="image-preview.png", preview_path=IMAGE_PREVIEW
    )

    assert preview == True
    assert os.path.exists("image-preview.png") == True

    await tracemoe.aio_session.close()


async def test_e_errors():
    tracemoe = AsyncTrace(api_token="spfskjapofapokfapkf")

    with pytest.raises(InvalidToken):
        await tracemoe.get_me()

    with pytest.raises(InvalidToken):
        await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)

    await tracemoe.aio_session.close()

    tracemoe = AsyncTrace()

    with pytest.raises(ServerError):
        await tracemoe.search("https://example.com")

    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)

    with pytest.raises(InvalidPath):
        await result.docs[0].save("preview.mp4", preview_path="/non-existant-path")

    await tracemoe.aio_session.close()
