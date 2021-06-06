# TraceMoePY

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aaed48cb31674d86b9e1355d8b78f855)](https://app.codacy.com/gh/DragSama/tracemoepy?utm_source=github.com&utm_medium=referral&utm_content=DragSama/tracemoepy&utm_campaign=Badge_Grade)
[![PyPI version](https://img.shields.io/pypi/v/tracemoepy?color=bright-green)](https://pypi.org/project/tracemoepy/)
[![Downloads](https://img.shields.io/pypi/dd/tracemoepy)](https://pypi.org/project/tracemoepy/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install
- Install using pip: `pip install tracemoepy`

### Examples
- All the examples below are after this piece of code:
```python
import tracemoepy
tracemoe = tracemoepy.tracemoe.TraceMoe()
```

- Search image using url:
```python
resp = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
print(resp.prettify())
print(f"Match: {resp.result[0].anilist.title.romaji}\nSimilarity: {resp.result[0].similarity*100}")
```

- Or just file path:
```python
print(tracemoe.search('image.jpg', upload_file=True))
```
- Save Video Preview:
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
output.result[0].save('preview.mp4', mute = False) # True for silent
```
- Save Video preview (2)
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
video = tracemoe.natural_preview(output)
with open('preview.mp4', 'wb') as f:
  f.write(video)
```
- Save Image Preview
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
output.result[0].save(save_path = 'preview.png', preview_type="image")
```
- Image Preview (Method 2)
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
tracemoe.image_preview(output) # Gives content
```
- You can do help(method_name) to get more info about the given method
```python
help(tracemoe.search)
```
#### Asyncio
**All the examples below assume you are running this inside a async function**

- Basic search (AioHttp session is not closed, You can access it as .aio_session)
```python
import tracemoepy
tracemoe = tracemoepy.AsyncTrace()
resp = await tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
print(f"Match: {resp.result[0].anilist.title.romaji}\nSimilarity: {resp.result[0].similarity*100}")
```   

- Auto close session
```python
import tracemoepy
async with tracemoepy.AsyncTrace() as tracemoe:
  resp = await tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
  print(f"Match: {resp.result[0].anilist.title.romaji}\nSimilarity: {resp.result[0].similarity*100}")

```
#### Errors

  - `TooManyRequests`: Raised when API Limit is reached or Too many requests in short period of time.
  - `EntityTooLarge`: Raised when image size is greater than max size of 10MB.
  - `ServerError`: Raised when Something wrong with the trace.moe server or Image provided was malformed.
  - `InvalidToken`: Raised when Invalid token was provided.
  - `EmptyImage`: Raised when Image provided was empty.
  - `InvalidPath`: Invalid path was given, This is only raised by `.save(...)` method
  - All these errors are located at tracemoepy.errors, Example of handling Exception:
```python
from tracemoepy.errors import TooManyRequests

try:
  # Do something
except TooManyRequests as t:
  print(t)
  # Do something if error
```
