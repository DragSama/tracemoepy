# tracemoepy
trace.moe python wrapper, does not support all api methods yet.
Work in progress.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/527bf31631e3494493951dda87479d9b)](https://www.codacy.com/manual/DragSama/tracemoepy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DragSama/tracemoepy&amp;utm_campaign=Badge_Grade)

[![PyPI version](https://img.shields.io/pypi/v/tracemoepy?color=bright-green)](https://pypi.org/project/tracemoepy/)
[![Downloads](https://img.shields.io/pypi/dd/tracemoepy)](https://pypi.org/project/tracemoepy/)

# Install
- Install using pip: `pip install tracemoepy`

# Examples
- All the examples below are after this piece of code:
```python
import tracemoepy
tracemoe = tracemoepy.tracemoe.TraceMoe()
```

- You can search image like:
```python
print(tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True))
```

- Or if you provide base64 encoded image:
```python
print(tracemoe.search(image, encode=False))
```
- Or if you want to just provide the image, The wrapper will encode image using base64:
```python
print(tracemoe.search('a.jpg', encode=True))
```
- Video Preview (Gives content):
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
tracemoe.video_preview(output)
```
- Save video preview
```python
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
video = tracemoe.video_preview(output)
with open('preview.mp4', 'wb') as f:
  f.write(video)
```
## Asyncio
```python
import tracemoepy
import asyncio
tracemoe = tracemoe.asynctrace.Async_Trace()
async def anything():
   #return await + Anything from the above examples
   #like:
   return await tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
loop = asyncio.get_event_loop()
loop.run(anything())
```   
# Errors

- `TooManyRequests`: Raised when API Limit is reached or Too many requests in short period of time.
- `EntityTooLarge`: Raised when image size is greater than max size of 10MB.
- `ServerError`: Raised when Something wrong with the trace.moe server or Image provided was malformed.
- `InvalidToken`: Raised when Invalid token was provided.
- `EmptyImage`: Raised when Image provided was empty.
- All these errors are located at tracemoepy.errors, Example of handling Exception:
```python
from tracemoepy.errors import TooManyRequests

try:
  # Do something
except TooManyRequests as t:
  print(t)
  # Do something if error
```
