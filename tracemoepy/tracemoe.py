from .helpers.constants import BASE_URL, BASE_MEDIA_URL, IMAGE_PREVIEW, VIDEO_PREVIEW
from .errors import EmptyImage, InvalidToken, ServerError, TooManyRequests, InvalidPath

from typing import Union, Optional
from base64 import b64encode
from urllib.parse import quote

from attrify import Attrify

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
        url = json['video']
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

    def get_me(self) -> Attrify:
        """
        Lets you check the search quota and limit for your account (or IP address).
        Returns:
          Attrify: response from server
        """
        url = f"{self.base_url}/me"
        if self.api_token:
            url += f"?token={self.api_token}"
        response = requests.get(url)
        if response.status_code == 403:
            raise InvalidToken("You are using Invalid token!")
        if ujson:
            return Attrify(ujson.loads(response.text))
        return Attrify(response.json())

    def search(
        self,
        path: str,
        is_url: bool = False,
        upload_file: bool = False,
    ) -> Attrify:
        """
        Args:
           path: Image url or Img file name or base64 encoded Image or Image path
           is_url: Treat the path as a url or not
           upload_file: Upload file
        Returns:
           Attrify: response from server
        Raises:
           EmptyImage: Raised If Image Is empty
           InvalidToken: Raised when token provided Is Invalid
           ServerError: Raised If server Is having problem or Image Is malformed.
           TooManyRequests: Raised If you make too many requests to server.
        """
        url = f"{self.base_url}/search"
        if self.api_token:
            url += f"?token={self.api_token}"

        if is_url:
            response = requests.get(url, params={"url": path})
        elif upload_file:
            with open(path, "rb") as f:
                response = requests.post(url, files={"image": f})
        else:
            response = requests.post(url, json={"image": path})
        if response.status_code == 200:
            if ujson:
                json = Attrify(ujson.loads(response.text))
            else:
                json = Attrify(response.json())
            for entry in json.result:
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

    def image_preview(self, response: Union[dict, Attrify], index: int = 0) -> bytes:
        """
        Args:
           response: Response returned by search
           index: Which result to get
        Returns:
           bytes: Image content
        """
        return requests.get(response["result"][index]["image"]).content

    def video_preview(self, response: Union[dict, Attrify], index: int = 0, mute: bool = False) -> bytes:
        """
        Args:
           response: Python dict given by search
           index: Which result to get
           mute: The given video should be mute or not.
        Returns:
           bytes: Video content
        """
        return requests.get(response["result"][index]["video"] + ("&mute" if mute else "")).content

    def natural_preview(self, *args, **kwargs) -> bytes:
        """
         Same as tracemoe.video_preview since v4.
        """
        return self.video_preview(*args, **kwargs)
