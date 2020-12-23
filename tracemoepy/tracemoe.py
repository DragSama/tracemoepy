from .helpers.superdict import convert, SuperDict
from .helpers.constants import BASE_URL, BASE_MEDIA_URL, IMAGE_PREVIEW, VIDEO_PREVIEW
from .errors import EmptyImage, InvalidToken, ServerError, TooManyRequests, InvalidPath

from typing import Union, Optional
from base64 import b64encode
from urllib.parse import quote

import requests
import types

try:
    import ujson
except ImportError:
    ujson = False


def save(self, save_path: str, preview_path: Optional[str] = None, mute: bool = False):
    """
    Save preview in given location
    Args:
        save_path: Path to save preview
        preview_path: None for natural preview, Otherwise preview.php or thumbnail.php, Defaults to None
        mute: Mute natural preview, Defaults to False
    Raises:
        ServerError: Failed to create preview
        InvalidPath: Preview path given doesn't exist on tracemoe servers
    """
    json = self
    if preview_path:
        url = (
            f"{BASE_URL}{preview_path}?anilist_id={json['anilist_id']}"
            f"&file={quote(json['filename'])}&t={json['at']}&token={json['tokenthumb']}"
        )
    else:
        url = (
            f'{BASE_MEDIA_URL}video/{json["anilist_id"]}/'
            f'{quote(json["filename"])}?t={json["at"]}&token={json["tokenthumb"]}'
        )
        if mute:
            url += "&mute"
    response = requests.get(url)
    if response.status_code in [500, 503]:
        raise ServerError("Image is malformed or Something went wrong")
    elif response.status_code in [404]:
        raise InvalidPath(f"Path {preview_path} doesn't exist on {BASE_URL}.")
    with open(save_path, "wb") as file:
        file.write(response.content)
    return True


class TraceMoe:

    """Tracemoe class with all the stuff."""

    def __init__(self, api_token: str = "") -> None:
        """Setup all vars."""
        self.base_url = BASE_URL
        self.media_url = BASE_MEDIA_URL
        self.api_token = api_token

    def get_me(self) -> SuperDict:
        """
        Lets you check the search quota and limit for your account (or IP address).
        Returns:
          SuperDict: response from server
        """
        url = f"{self.base_url}api/me"
        if self.api_token:
            url += f"?token={self.api_token}"
        response = requests.get(url)
        if response.status_code == 403:
            raise InvalidToken("You are using Invalid token!")
        if ujson:
            return convert(ujson.loads(response.text))
        return convert(response.json())

    def search(
        self,
        path: str,
        encode: bool = False,
        is_url: bool = False,
        upload_file: bool = False,
    ) -> SuperDict:
        """
        Args:
           path: Image url or Img file name or base64 encoded Image or Image path
           encode: True if Img file name is given
           is_url: Treat the path as a url or not
           upload_file: Upload file
        Returns:
           SuperDict: response from server
        Raises:
           EmptyImage: Raised If Image Is empty
           InvalidToken: Raised when token provided Is Invalid
           ServerError: Raised If server Is having problem or Image Is malformed.
           TooManyRequests: Raised If you make too many requests to server.
        """
        url = f"{self.base_url}api/search"
        if self.api_token:
            url += f"?token={self.api_token}"

        if is_url:
            response = requests.get(url, params={"url": path})
        elif upload_file:
            with open(path, "rb") as f:
                response = requests.post(url, files={"image": f})
        elif encode:
            with open(path, "rb") as f:
                encoded = b64encode(f.read()).decode("utf-8")
                response = requests.post(url, json={"image": encoded})
        else:
            response = requests.post(url, json={"image": path})
        if response.status_code == 200:
            if ujson:
                json = convert(ujson.loads(response.text))
            else:
                json = convert(response.json())
            for entry in json.docs:
                entry.save = types.MethodType(save, entry)
            return json
        elif response.status_code == 400:
            raise EmptyImage("Image provided was empty!")
        elif response.status_code == 403:
            raise InvalidToken("You are using Invalid token!")
        elif response.status_code in [500, 503]:
            raise ServerError("Image is malformed or Something went wrong")
        elif response.status_code == 429:
            raise TooManyRequests(response.text)
        else:
            raise ServerError(f"Unknown error: {response.status_code}")

    def create_preview(
        self, json: Union[dict, SuperDict], path: str, index: int = 0
    ) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
           path: Path to use, preview.php, thumbnail.php etc.
        Returns:
           bytes: Video/Image content
        """
        json = json["docs"][index]
        url = (
            f"{self.base_url}{path}?anilist_id={json['anilist_id']}"
            f"&file={quote(json['filename'])}&t={json['at']}&token={json['tokenthumb']}"
        )
        response = requests.get(url)
        if response.status_code in [500, 503]:
            raise ServerError("Image is malformed or Something went wrong")
        else:
            return response.content

    def image_preview(self, json: Union[dict, SuperDict], index: int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           bytes: Video content
        """
        return self.create_preview(json, "thumbnail.php", index)

    def video_preview(self, json: Union[dict, SuperDict], index: int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           bytes: Video content
        """
        return self.create_preview(json, "preview.php", index)

    def natural_preview(
        self, response: Union[dict, SuperDict], index: int = 0, mute: bool = False
    ) -> bytes:
        """
        Video Preview with Natural Scene Cutting
        Args:
            response: server response
            index: which result to pick
            mute: mute video or not.
        Returns:
            bytes: Video content
        """
        response = response["docs"][index]
        url = (
            f'{self.media_url}video/{response["anilist_id"]}/'
            f'{quote(response["filename"])}?t={response["at"]}&token={response["tokenthumb"]}'
        )
        if mute:
            url += "&mute"
        response = requests.get(url)
        if response.status_code in [500, 503]:
            raise ServerError("Image is malformed or Something went wrong")
        else:
            return response.content
