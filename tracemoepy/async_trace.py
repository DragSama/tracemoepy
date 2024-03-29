from .helpers.constants import BASE_URL, BASE_MEDIA_URL, IMAGE_PREVIEW, VIDEO_PREVIEW
from .errors import EmptyImage, InvalidToken, ServerError, TooManyRequests, InvalidPath

from typing import Union, Optional
from base64 import b64encode
from urllib.parse import quote

from attrify import Attrify

try:
    import ujson
except ImportError:
    ujson = False

import aiohttp
import types


async def save(
    self, save_path: str, preview_type: Optional[str] = None, mute: bool = False
):
    """
    Save preview in given location
    Args:
        save_path: Path to save preview
        preview_type: image/video
        mute: Mute natural preview, Defaults to False
    Raises:
        ServerError: Failed to create preview
        InvalidPath: Preview path given doesn't exist on tracemoe servers
    """
    json = self
    if not preview_type or preview_type == "video":
        url = json['video']
        if mute:
            url += "&mute"
    elif preview_type and preview_type == "image":
        url = json['image']
    else:
        raise InvalidPath("'preview_type' can only be 'image' or 'video'")
    response = await self.aio_session.get(url)
    if response.status in [500, 503]:
        raise ServerError("Image is malformed or Something went wrong")
    elif response.status in [404]:
        raise InvalidPath(f"Path {preview_path} doesn't exist on {BASE_URL}.")
    with open(save_path, "wb") as file:
        file.write((await response.content.read()))
    return True


class AsyncTrace:

    """Tracemoe class with all the stuff."""

    def __init__(
        self, api_token: str = "", session: Union[aiohttp.ClientSession, bool] = False
    ):
        """Setup all urls and session."""
        self.base_url = BASE_URL
        self.media_url = BASE_MEDIA_URL
        self.api_token = api_token
        if not session:
            self.aio_session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"}
            )
        else:
            self.aio_session = session

    async def get_me(self) -> Attrify:
        """
        Lets you check the search quota and limit for your account (or IP address).
        Returns:
          Attrify: response from server
        """
        url = f"{self.base_url}/me"
        if self.api_token:
            url += f"?key={self.api_token}"
        response = await self.aio_session.get(url)
        if response.status == 403:
            raise InvalidToken("You are using Invalid token!")
        if ujson:
            return Attrify((await response.json(loads=ujson.loads)))
        return Attrify((await response.json()))

    async def search(
        self,
        path: str,
        is_url: bool = False,
        upload_file: bool = False,
        cut_black_borders: bool = True,
        include_anilist_info: bool = True
    ) -> Attrify:
        """
        Args:
           path: Image url or Img file name or base64 encoded Image or Image path.
           is_url: Treat the path as a url or not.
           upload_file: Self explanatory.
           cut_black_borders: trace.moe can detect black borders automatically and cut away unnecessary parts of the images that would affect search results accuracy.
           include_anilist_info: Additional info about anime.
        Returns:
           Attrify: response from server
        Raises:
           EmptyImage: Raised If Image Is empty
           InvalidToken: Raised when token provided Is Invalid
           ServerError: Raised If server Is having problem or Image Is malformed.
           TooManyRequests: Raised If you make too many requests to server.
        """
        url = f"{self.base_url}/search"
        params = {}
        if self.api_token:
            params['key']= self.api_token
        if cut_black_borders:
            params['cutBorders'] = ""
        if include_anilist_info:
            params['anilistInfo'] = ""

        if is_url:
            params['url'] = path
            response = await self.aio_session.get(url, params=params)
        elif upload_file:
            with open(path, "rb") as file:
                response = await self.aio_session.post(
                    url, data={"image": file},params=params
                )
        else:
            response = await self.aio_session.post(url, json={"image": path}, params=params)
        if response.status == 200:
            if ujson:
                json = Attrify((await response.json(loads=ujson.loads)))
            else:
                json = Attrify((await response.json()))
            for entry in json.result:
                entry.aio_session = self.aio_session
                entry.save = types.MethodType(save, entry)
            return json
        elif response.status == 400:
            raise EmptyImage("Image provided was empty!")
        elif response.status == 403:
            raise InvalidToken("You are using Invalid token!")
        elif response.status in [500, 503]:
            raise ServerError("Image is malformed or Something went wrong")
        elif response.status == 429:
            raise TooManyRequests(response.text)
        else:
            raise ServerError(f"Unknown error: {response.status}, {response.url}")

    async def natural_preview(self, *args, **kwargs) -> bytes:
        return await self.video_preview(*args, **kwargs)
        

    async def image_preview(
        self, response: Union[dict, Attrify], index: int = 0
    ) -> bytes:
        """
        Args:
           response: Response returned by search
           index: Which result to get
        Returns:
           bytes: Image content
        """
        return await (await self.aio_session.get(response["result"][index]["image"])).content.read()

    async def video_preview(
        self, response: Union[dict, Attrify], index: int = 0, mute: bool=False) -> bytes:
        """
        Args:
           response: Response returned by search
           index: Which result to get
           mute: The given video should be mute or not.
        Returns:
           bytes: Video content
        """
        return await (await self.aio_session.get(response["result"][index]["video"] + ("&mute" if mute else ""))).content.read()
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.aio_session.close()

Async_Trace = AsyncTrace
