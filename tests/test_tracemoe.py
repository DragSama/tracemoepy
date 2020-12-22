import unittest
import os

from tracemoepy import TraceMoe
from tracemoepy.errors import (
    EmptyImage,
    InvalidToken,
    ServerError,
    TooManyRequests,
    InvalidPath
)
from tracemoepy.helpers.superdict import SuperDict
from tracemoepy.helpers.constants import IMAGE_PREVIEW

class test_tracemoe(unittest.TestCase):

    def test_search(self):

        tracemoe = TraceMoe()

        result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)
        self.assertIsInstance(result, SuperDict)

        result = tracemoe.search('flipped-good.webp', upload_file = True)
        self.assertIsInstance(result, SuperDict)

        # Not testing because tracemoe is having issues with base64 encoded images.
        #result = tracemoe.search('flipped-good.webp', encode = True)
        #self.assertIsInstance(result, SuperDict)

    def test_natural_preview(self):

        tracemoe = TraceMoe()
        result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

        content = tracemoe.natural_preview(result)
        self.assertIsInstance(content, bytes)

        preview = result.docs[0].save('natural-preview.mp4')
        self.assertEqual(preview, True)
        self.assertEqual(os.path.exists('natural-preview.mp4'), True)

        preview = result.docs[0].save('natural-preview-silent.mp4', mute = True)
        self.assertEqual(preview, True)
        self.assertEqual(os.path.exists('natural-preview-silent.mp4'), True)

    def test_image_preview(self):
        tracemoe = TraceMoe()
        result = tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

        content = tracemoe.image_preview(result)
        self.assertIsInstance(content, bytes)

        preview = result.docs[0].save(save_path='image-preview.png', preview_path=IMAGE_PREVIEW)
        self.assertEqual(preview, True)
        self.assertEqual(os.path.exists('image-preview.png'), True)

    def test_errors(self):
        tracemoe = TraceMoe(api_token = 'spfskjapofapokfapkf')
        with self.assertRaises(InvalidToken):
            tracemoe.get_me()
        with self.assertRaises(InvalidToken):
            tracemoe.search('https://trace.moe/img/flipped-good.jpg', is_url = True)

        tracemoe = TraceMoe()

        with self.assertRaises(EmptyImage):
            tracemoe.search('https://example.com')


if __name__ == '__main__':
    unittest.main()
