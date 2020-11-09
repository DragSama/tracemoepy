from base64 import b64encode
from urllib.parse import quote

import aiohttp

from .errors import EmptyImage, InvalidToken, ServerError, TooManyRequests
from .customs import convert


class Async_Trace:

    """Tracemoe class with all the stuff."""

    def __init__(self, api_token: str = "", session=False):
        """Setup all urls and session."""
        self.base_url = "https://trace.moe/"
        self.media_url = "https://media.trace.moe/"
        self.api_token = api_token
        if not session:
            self.aio_session = aiohttp.ClientSession()
        else:
            self.aio_session = session
        self.aio_session.headers = {"Content-Type": "application/json"}

    async def get_me(self) -> dict:
        """
        Lets you check the search quota and limit for your account (or IP address).
        Returns:
          dict: response from server
        """
        url = f"{self.base_url}me"
        if self.api_token:
            url += f"?token={self.token}"
        return await (await self.aio_session.get(url)).json()

    async def search(self, path: str, encode: bool = False, upload_file=False, is_url: bool = False) -> dict:
        """
        Args:
           path: Image url or Img file name or base64 encoded Image or Image path
           encode: True if Img file name is given
           is_url: Treat the path as a url or not
           upload_file: Upload file
        Returns:
           dict: response from server
        Raises:
           EmptyImage: Raised If Image Is empty
           InvalidToken: Raised when token provided Is Invalid
           ServerError: Raised If server Is having problem or Image Is malformed.
           TooManyRequests: Raised when you are making too many requests
        """
        url = f"{self.base_url}api/search"
        if self.api_token:
            url += f"?token={self.api_token}"

        if is_url:
            response = await self.aio_session.get(
                url, params={"url": path}
            )
        elif upload_file:
            response = await self.aio_session.post(
                'https://trace.moe/api/search',
                data={'image': open(path, 'rb')}
            )
        elif encode:
            with open(path, "rb") as f:
                encoded = b64encode(f.read()).decode("utf-8")
                response = await self.aio_session.post(
                    url, json={"image": encoded}
                )
        else:
            response = await self.aio_session.post(
                url, json={"image": encoded}
            )
        if response.status == 200:
            return convert((await response.json()))
        elif response.status == 400:
            raise EmptyImage('Image provided was empty!')
        elif response.status == 403:
            raise InvalidToken('You are using Invalid token!')
        elif response.status in [500, 503]:
            raise ServerError('Image is malformed or Something went wrong')
        elif response.status == 429:
            raise TooManyRequests(await response.text)
        else:
            raise ServerError(f'Unknown error: {response.status}')

    async def create_preview(self, json: dict, path: str, index: int = 0,) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
           path: Path to use, preview.php, thumbnail.php etc.
        Returns:
           bytes: Video/Image content
        """
        json = json["docs"][index]
        url = f"{self.base_url}{path}?anilist_id={json['anilist_id']}"\
              f"&file={quote(json['filename'])}&t={json['at']}&token={json['tokenthumb']}"
        return await (await self.aio_session.get(url)).content.read()

    async def natural_preview(self, response: dict, index: int = 0, mute: bool = False) -> bytes:
        """
        Video Preview with Natural Scene Cutting
        Args:
            response: server response
            index: which result to get
            mute: mute video or not.
        Returns:
            bytes: Video content
        """
        response = response["docs"][index]
        url = f'{self.media_url}video/{response["anilist_id"]}/'\
              f'{quote(response["filename"])}?t={response["at"]}&token={response["tokenthumb"]}'
        if mute:
            url += "&mute"
        return await (await self.aio_session.get(url)).content.read()

    async def image_preview(self, json: dict, index: int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           bytes: Video content
        """
        return await self.create_preview(json, 'thumbnail.php', index)

    async def video_preview(self, json: dict, index: int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           bytes: Video content
        """
        return await self.create_preview(json, 'preview.php', index)
