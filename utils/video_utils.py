import os
import subprocess
import shutil
import re
import glob

import cv2 as cv
import imageio
from .constants import *
from .utils import build_image_name


# Return frame names that follow the 6 digit pattern and have .jpg extension
def valid_frames(input_dir):
    def valid_frame_name(str):
        pattern = re.compile(r'[0-9]{6}\.jpg')  # regex, examples it covers: 000000.jpg or 923492.jpg, etc.
        return re.fullmatch(pattern, str) is not None
    candidate_frames = sorted(os.listdir(input_dir))
    valid_frames = list(filter(valid_frame_name, candidate_frames))
    return valid_frames


def create_video_name(config):
    prefix = 'video_' if config['input_name'].endswith('.mp4') else 'ouroboros_video_'

    infix = build_image_name(config).rsplit('.', 1)[0]  # remove the .jpg suffix

    blend_info = f'blend_{config["blend"]}_' if config['input_name'].endswith('.mp4') else ''  # not used for Ouroboros
    video_specific_infix = f'fps_{config["fps"]}_{blend_info}'

    suffix = '.mp4'

    video_name = prefix + video_specific_infix + infix + suffix
    return video_name


def create_video_from_intermediate_results(config):
    width = config['img_dimensions'][1]
    height = config['img_dimensions'][0]
    video_path = os.path.join(OUT_VIDEOS_PATH, create_video_name(config))
    out = cv.VideoWriter(video_path, cv.VideoWriter_fourcc(*'mp4v'), config['fps'], (width, height))
    for img in sorted(glob.glob(config['dump_dir']+'/*.jpg')):
        frame = cv.imread(img)
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        out.write(frame)
    out.release()



def extract_frames(video_path, dump_dir):
    ffmpeg = 'ffmpeg'
    if shutil.which(ffmpeg):  # if ffmpeg is in the system path
        cap = cv.VideoCapture(video_path)
        fps = int(cap.get(cv.CAP_PROP_FPS))

        input_options = ['-i', video_path]
        extract_options = ['-r', str(fps)]
        out_frame_pattern = os.path.join(dump_dir, 'frame_%6d.jpg')
        less_verbose = ['-loglevel', 'warning']

        subprocess.call([ffmpeg, *input_options, *extract_options, *less_verbose, out_frame_pattern])

        print(f'Dumped frames to {dump_dir}.')
        metadata = {'pattern': out_frame_pattern, 'fps': fps}
        return metadata
    else:
        raise Exception(f'{ffmpeg} not found in the system path, aborting.')


def create_gif(frames_dir, out_path):
    assert os.path.splitext(out_path)[1].lower() == '.gif', f'Expected gif got {os.path.splitext(out_path)[1]}.'

    frame_paths = [os.path.join(frames_dir, frame_name) for frame_name in sorted(os.listdir(frames_dir)) if frame_name.endswith('.jpg')]
    images = [imageio.imread(frame_path) for frame_path in frame_paths]
    imageio.mimwrite(out_path, images, fps=10)
    print(f'Saved gif to {out_path}.')
