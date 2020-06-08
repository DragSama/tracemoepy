# tracemoepy
trace.moe python wrapper, does not support all api methods yet.
Work in progress.

[![PyPI version](https://img.shields.io/pypi/v/tracemoepy?color=bright-green)](https://img.shields.io/pypi/v/tracemoepy?color=bright-green)
[![Downloads](https://img.shields.io/pypi/dd/tracemoepy)](https://img.shields.io/pypi/dd/tracemoepy)

# Install
- Install using pip: `pip install tracemoepy`

# Examples
- All the examples below are after this piece of code:
```
import tracemoepy
tracemoe = tracemoepy.tracemoe.TraceMoe()
```

- You can search image like:
```
print(tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True))
```
- Or if you provide base64 encoded image:
```
print(tracemoe.search(image, encode=False))
```
- Or if you want to just provide the image, The wrapper will encode image using base64:
```
print(tracemoe.search('a.jpg', encode=True))
```
- Video Preview (Gives content):
```
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
tracemoe.video_preview(output)
```
- Save video preview
```
output = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
video = tracemoe.video_preview(output)
with open('preview.mp4', 'wb') as f:
  f.write(video)
```
