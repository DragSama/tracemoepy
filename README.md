# TraceMoePY

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aaed48cb31674d86b9e1355d8b78f855)](https://app.codacy.com/gh/DragSama/tracemoepy?utm_source=github.com&utm_medium=referral&utm_content=DragSama/tracemoepy&utm_campaign=Badge_Grade)
[![PyPI version](https://img.shields.io/pypi/v/tracemoepy?color=bright-green)](https://pypi.org/project/tracemoepy/)
[![Downloads](https://img.shields.io/pypi/dd/tracemoepy)](https://pypi.org/project/tracemoepy/)
[![Github Actions](https://github.com/DragSama/tracemoepy/workflows/Github%20Actions/badge.svg)](https://github.com/DragSama/tracemoepy/actions)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install
- Install using pip: `pip install tracemoepy`

### Examples
- All the examples below are after this piece of code:
```python
import tracemoepy
tracemoe = tracemoepy.tracemoe.TraceMoe()
```

- You can search image like:
```python
result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
print(result.prettify())
print(f'{result.docs[0].title}')
```

- Or if you provide base64 encoded image:
```python
print(tracemoe.search(image, encode=False))
```
- Or if you want to just provide the image, The wrapper will encode image using base64:
```python
print(tracemoe.search('a.jpg', encode=True))
```
- Natural Preview:
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
output.docs[0].save('preview.mp4', mute = False) # True for silent
```
- Save Natural preview (Method 2)
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
video = tracemoe.natural_preview(output)
with open('preview.mp4', 'wb') as f:
  f.write(video)
```
- Save Image Preview
```python
from tracemoepy.helpers.constants import IMAGE_PREVIEW
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
output.docs[0].save(save_path = 'preview.png', preview_path = IMAGE_PREVIEW)
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
```python
import tracemoepy
import asyncio
# It recommended is you provide your own aiohttp session as
# tracemoepy will NOT close the session, You can access the session
# like: tracemoe.aio_session, To provide own aiohttp session you can just do
# tracemoe.AsyncTrace(session = your_session)
tracemoe = tracemoepy.AsyncTrace()
async def anything():
   return await tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
loop = asyncio.get_event_loop()
loop.run_until_complete(anything())
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
