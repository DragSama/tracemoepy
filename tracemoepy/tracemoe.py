from base64 import b64encode
from requests import Session
from .errors import EmptyImage, InvalidToken, ServerError, TooManyRequests

class TraceMoe:
    """Tracemoe class with all the stuff"""
    def __init__(self, api_token:str=""):
        self.base_url = "https://trace.moe/"
        self.media_url = "https://media.trace.moe/"
        self.api_token = api_token
        self.r_session = Session()
        self.r_session.headers = {"Content-Type": "application/json"}
    
    def get_me(self) -> dict:
        """
        Lets you check the search quota and limit for your account (or IP address).
        Returns:
          dict: response from server
        """
        url = f"{self.base_url}me"
        if self.api_token: url += f"?token={self.token}"
        return self.r_session.get(url).json()
    
    def search(self, path:str, encode:bool=True, is_url:bool=False) -> dict:
        """
        Args:
           path: Image url or Img file name or base64 encoded Image
           encode: True if Img file name is given
           is_url: Treat the path as a url or not
        Returns:
           dict: response from server
        Raises:
           EmptyImage: Raised If Image Is empty
           InvalidToken: Raised when token provided Is Invalid
           ServerError: Raised If server Is having problem or Image Is malformed.
        """
        url = f"{self.base_url}api/search"
        if self.api_token:
            url += f"?token={self.api_token}"

        if is_url:
            return self.r_session.get(
                url, params={"url": path}
            ).json()

        elif encode:
            with open(path, "rb") as f:
                encoded = b64encode(f.read()).decode("utf-8")
                response = self.r_session.post(
                url, json={"image": encoded}
                )
        else:
            response = self.r_session.post(
                url, json={"image": encoded}
                )
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            raise EmptyImage('Image provided was empty!')
        elif response.status_code == 403:
            raise InvalidToken('You are using Invalid token!')
        elif response.status_code in [500, 503]:
            raise ServerError('Image is malformed or Something went wrong')
        elif response.status_code == 429:
            raise TooManyRequests(response.text)
    
    def create_preview(self, json:dict, path:str, index:int = 0,) -> bytes:
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
              f"&file={json['filename']}&t={json['at']}&token={json['tokenthumb']}"
        print(url)
        return self.r_session.get(url).content
    
    def image_preview(self, json:dict, index:int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           bytes: Video content
        """
        return self.create_preview(json, 'thumbnail.php', index)
    
    def video_preview(self, json:dict, index:int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           bytes: Video content
        """
        return self.create_preview(json, 'preview.php', index)
        
        
