import argparse

from thumbnail_pipeline import ThumbnailsAssetPipeline


def main():
    parser = argparse.ArgumentParser(
        description='Capture specific number of frames from video.')
    parser.add_argument('--input', help='path to video', type=str)
    parser.add_argument('--output', help='output path', type=str)
    parser.add_argument('--thumb_num', help='number of thumbnails', type=int,
                        default=3)

    args = parser.parse_args()
    asset_pipeline = ThumbnailsAssetPipeline()
    asset_pipeline.execute(
        {
            'input': args.input,
            'output': args.output,
            'thumb_num': args.thumb_num
        }
    )


if __name__ == "__main__":
    main()
