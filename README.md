# tracemoepy
trace.moe python wrapper, does not support all api methods yet.
Work in progress.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/afb292fa1406455e8c804bfdd18f5eb7)](https://app.codacy.com/manual/DragSama/tracemoepy?utm_source=github.com&utm_medium=referral&utm_content=DragSama/tracemoepy&utm_campaign=Badge_Grade_Dashboard)
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
