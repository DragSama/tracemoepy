from base64 import b64encode
from requests import Session

class TraceMoe:
    """Tracemoe class with all the stuff"""
    def __init__(self, api_token:str=""):
        self.base_url = "https://trace.moe/"
        self.media_url = "https://media.trace.moe/"
        self.api_token = api_token
        self.r_session = Session()
        self.r_session.headers = {
            "Content-Type": "application/json"
        }
    
    def search(self, path:str, encode:bool=True, is_url:bool=False) -> dict:
        """
        Args:
           path: Image url or Img file name or base64 encoded Image
           encode: True if Img file name is given
           is_url: Treat the path as a url or not
        Returns:
           json response
        """
        url = f"{self.base_url}/api/search"
        if self.api_token:
            url += f"?token={self.api_token}"

        if is_url:
            return self.r_session.get(
                url, params={"url": path}
            ).json()

        elif encode:
            with open(path, "rb") as f:
                encoded = b64encode(f.read()).decode("utf-8")
                return self.r_session.post(
                url, json={"image": encoded}
                ).json()
        else:
            return self.r_session.post(
                url, json={"image": encoded}
                ).json()
    
    def create_preview(self, json:dict, path:str, index:int = 0,) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
           path: Path to use, preview.php, thumbnail.php etc.
        Returns:
           Image content
        """
        json = json["docs"][index]
        url = f"{self.base_url}/{path}?anilist_id={json['anilist_id']}"\
              f"&file={json['filename']}&t={json['at']}&token]{json['tokenthumb']}"
        return self.r_session.get(url).content
    
    def video_preview(self, json:dict, index:int = 0) -> bytes:
        """
        Args:
           json: Python dict given by search
           index: Which result to get
        Returns:
           Image content
        """
        return self.create_preview(json, 'preview.php', index)
        
        
        
