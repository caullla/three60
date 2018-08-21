import filecmp
import shutil
import unittest

from thumbnail_pipeline import ThumbnailsAssetPipeline


class ThumbnailTestCase(unittest.TestCase):
    def test_frame_steps(self):
        pipeline = ThumbnailsAssetPipeline()
        frames = pipeline.get_frames(10, 3)
        self.assertEqual(frames, [1, 4, 7])

    def test_frame_too_many_thumbs(self):
        pipeline = ThumbnailsAssetPipeline()
        self.assertRaises(ValueError, pipeline.get_frames, 10, 11)

    def test_capture_thumnails(self):
        pipeline = ThumbnailsAssetPipeline()
        results = pipeline.capture_thumnails(
            input_path='test_assets/test.mp4',
            output_path='test_assets/test_run',
            thumb_num=1)
        self.assertTrue(filecmp.cmp(results[0], 'test_assets/out/test.mp4_7.png'))
        shutil.rmtree('test_assets/test_run/')


if __name__ == '__main__':
    unittest.main()
