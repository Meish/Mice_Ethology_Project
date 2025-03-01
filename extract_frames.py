# extract frames from a set of video files
"""
extract_frames.py
Arguments
input_dir   directory path to look for video files
output_dir  directory path to put extracted frames in as jpeg files
n_frames    total number of frames to capture across all the videos
to_skip     number of frames to skip at the beginning of each video
"""

from cv2 import VideoCapture, imwrite, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES
from glob import glob
from os.path import isdir, sep, split, splitext
from pathlib import Path
import argparse
import sys


def ensure_dir_exists(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def extract_frames_from_video(
    video_path, output_dir, sample_every, max_frames_to_extract, to_skip=0
):
    _, video_name = split(video_path)
    base, ext = splitext(video_name)
    pos = to_skip + (sample_every / 2.0)  # sample halfway through each range of frames
    extracted = 0
    try:
        vc = VideoCapture(video_path)
        if not vc.isOpened():
            print(f"video {video_path} is not readable, skipping")
            return
        frames = int(vc.get(CAP_PROP_FRAME_COUNT))
        while pos < frames - 1 and extracted < max_frames_to_extract:
            output_path = output_dir + sep + base + "_{:06d}.jpg".format(int(pos))
            vc.set(CAP_PROP_POS_FRAMES, int(pos))
            retval, img = vc.read()
            if retval:
                imwrite(output_path, img)
                extracted += 1
            pos += sample_every
    except Exception as e:
        print(
            f"extract_frames_from_video encountered exception {e} while working on video {video_path}, frame {int(pos)}"
        )
    finally:
        vc.release()
    return extracted


def extract_frames(input_dir, output_dir, frames_to_extract, to_skip=0):
    total_frames = 0
    ensure_dir_exists(output_dir)
    input_files = glob(input_dir + sep + "*")

    # go through files in input_dir, counting frames from supported video files
    for f in input_files:
        _, ext = splitext(f)
        if not ext in (".mp4", ".avi", ".mov", ".mpeg"):
            print(f'Unsupported file extension "{ext}", skipping {f} on scan pass')
            continue
        try:
            print(f"ext is {ext}, trying to open {f}")
            vc = VideoCapture(f)
            if not vc.isOpened():
                print(f"video {f} is not readable, skipping")
                continue
            num_frames = int(vc.get(CAP_PROP_FRAME_COUNT))
            total_frames += max(0, num_frames - to_skip)
            print(f"Adding {num_frames}")
        except Exception as e:
            print(
                f"extract_frames encountered exception {e} while counting frames of video {f}"
            )
        finally:
            vc.release()

    sample_every = total_frames / frames_to_extract

    print(f"Total frames: {total_frames}, sampling every {sample_every} frames")

    # go through the same files again, extracting frames this time
    for f in input_files:
        _, ext = splitext(f)
        if not ext in (".mp4", ".avi", ".mov", ".mpeg"):
            continue
        print(
            f"Extracting no more than {frames_to_extract} frames from {f} ...",
            end="",
            flush=True,
        )
        extracted = extract_frames_from_video(
            f, output_dir, sample_every, frames_to_extract, to_skip
        )
        print(f" got {extracted}.")
        frames_to_extract -= extracted


if __name__ == "__main__":
    """
    extract_frames command line entry point
    Arguments:
        input_dir           Directory/folder to look for video files to extract frames from
        output_dir          Directory/folder to place extracted frames in.  Will be created if needed.
        frames_to_extract   Total number of frames to extract across all videos found
        frames_to_skip      Number of frames to skip at the beginning of each video. Default is 0.
    """

    parser = argparse.ArgumentParser(
        description="extract_frames command line", prog="extract_frames"
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="directory/folder to look for video files to extract frames from",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="directory/folder to place extracted frames in.  Will be created if needed.",
    )
    parser.add_argument(
        "frames_to_extract",
        type=int,
        help="total number of frames to extract across all videos found",
    )
    parser.add_argument(
        "-s",
        "--skip",
        dest="frames_to_skip",
        type=int,
        default=0,
        help="number of frames to skip at the beginning of each video",
    )
    args = parser.parse_args(sys.argv[1:])

    extract_frames(
        args.input_dir, args.output_dir, args.frames_to_extract, args.frames_to_skip
    )
