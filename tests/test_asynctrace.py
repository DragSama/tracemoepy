import os
import pytest
import aiohttp
import asyncio

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
    await asyncio.sleep(1)
    await tracemoe.aio_session.close()


async def test_c_natural_preview():
    tracemoe = AsyncTrace()

    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    content = await tracemoe.natural_preview(result)

    assert isinstance(content, bytes)
    await asyncio.sleep(1)
    preview = await result.result[0].save("natural-preview.mp4")

    assert preview == True
    assert os.path.exists("natural-preview.mp4") == True
    await asyncio.sleep(1)
    preview = await result.result[0].save("natural-preview-silent.mp4", mute=True)

    assert preview == True
    assert os.path.exists("natural-preview-silent.mp4") == True

    await tracemoe.aio_session.close()


async def test_d_image_preview():
    tracemoe = AsyncTrace()

    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    content = await tracemoe.image_preview(result)

    assert isinstance(content, bytes)
    await asyncio.sleep(1)
    preview = await result.result[0].save(
        save_path="image-preview.png", preview_type="image"
    )

    assert preview == True
    assert os.path.exists("image-preview.png") == True

    await tracemoe.aio_session.close()


async def test_e_errors():
    tracemoe = AsyncTrace()

    with pytest.raises(ServerError):
        await tracemoe.search("https://example.com")
    await asyncio.sleep(1)
    result = await tracemoe.search("https://trace.moe/img/flipped-good.jpg", is_url=True)
    await asyncio.sleep(1)
    with pytest.raises(InvalidPath):
        await result.result[0].save("preview.mp4", preview_type="/non-existant-type")

    await tracemoe.aio_session.close()
