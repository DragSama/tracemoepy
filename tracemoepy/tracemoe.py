from .helpers.superdict import convert, SuperDict
from .helpers.constants import BASE_URL, BASE_MEDIA_URL, IMAGE_PREVIEW, VIDEO_PREVIEW
from .errors import EmptyImage, InvalidToken, ServerError, TooManyRequests

from typing import Union
from base64 import b64encode
from urllib.parse import quote

import requests


class TraceMoe:

    """Tracemoe class with all the stuff."""

    def __init__(self, api_token: str = ""):
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
        url = f"{self.base_url}me"
        if self.api_token:
            url += f"?token={self.token}"
        return convert(requests.get(url).json())

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
            response = requests.post(url, files={"image": open(path, "rb")})
        elif encode:
            with open(path, "rb") as f:
                encoded = b64encode(f.read()).decode("utf-8")
                response = requests.post(url, json={"image": encoded})
        else:
            response = requests.post(url, json={"image": encoded})
        if response.status_code == 200:
            return convert(response.json())
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
        return requests.get(url).content

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
        return requests.get(url).content
