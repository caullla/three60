import cv2
import logging
import os

from equirec2perspec import EquirectangularConverted

logger = logging


class ThumbnailsAssetPipeline(object):

    def execute(self, asset_data):
        # convert posix path to whatever system we're on
        input_path = asset_data.get('input', None)
        output_path = asset_data.get('output', None)
        thumb_num = asset_data.get('thumb_num', None)

        logger.info(asset_data)
        logger.info('now starting capture thumbnails progress for file {}'.format(input_path))
        images = self.capture_thumnails(input_path, output_path, thumb_num)
        logger.info('converted to {}'.format(images))

        return images

    def validate_file(self, input_path):
        if not os.path.isfile(input_path):
            raise Exception("Provide video doesn't exists.")

        # TODO: extend file validation

    def capture_thumnails(self, input_path, output_path, thumb_num):
        self.validate_file(input_path)

        if output_path is None:
            raise Exception("Output path is required argument.")

        # create folder if missing
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if thumb_num is None:
            raise Exception("Thumbnail number is required argument.")
        thumb_num = int(thumb_num)

        results = []

        vidcap = cv2.VideoCapture(input_path)
        video_name = os.path.basename(input_path)
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        for frame in self.get_frames(frame_count, thumb_num):
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            success, image = vidcap.read()
            try:
                file_name = os.path.join(output_path, '{}_{}.png'.format(video_name, frame))
                flat_file_name = os.path.join(output_path, '{}_{}_flat.png'.format(video_name, frame))
                cv2.imwrite(file_name, image)
                flat_image = self.get_undistorted_image(image)
                cv2.imwrite(flat_file_name, flat_image)
                results.append(file_name)
            except Exception as e:
                logger.exception(e)
        return results

    def get_undistorted_image(self, image):
        converter = EquirectangularConverted(image)
        return converter.get_perspective_img(90, 0, 0, 320, 320)

    def get_frames(self, frame_count, thumb_num):
        """
        get exact frame index to be captured
        """

        if thumb_num > frame_count:
            raise ValueError("Can't capture more thumbnails than frames in video file")

        if thumb_num < 1:
            return []

        results = []
        thumb_step = frame_count / thumb_num
        frame = thumb_step / 2
        cnt = 0
        while cnt < thumb_num:
            results.append(frame)
            frame += thumb_step
            cnt += 1
        return results
