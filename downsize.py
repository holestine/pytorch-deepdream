import cv2 as cv
import glob

def create_video(video_path, images_path, fps=30, width=640, height=360):
    
    out = cv.VideoWriter(video_path, cv.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for img in sorted(glob.glob(images_path+'/*.jpg')):
        print(img)
        frame = cv.imread(img)
        frame = cv.resize(frame, (width,height))
        out.write(frame)
    out.release()

#create_video('./data/out-videos/picaso.mp4', './data/out-videos/tmp_out')


def resize_video(input_video_path, output_video_path, fps=30, width=360, height=640):
    input = cv.VideoCapture(input_video_path)
    ouput = cv.VideoWriter(output_video_path, cv.VideoWriter_fourcc(*'mp4v'), fps, (height,width))
    while True:
        success, frame = input.read()
        if not success:
            break
        frame = cv.resize(frame, (height,width),fx=0,fy=0, interpolation = cv.INTER_CUBIC)
        ouput.write(frame)
    input.release()
    ouput.release()

resize_video('./data/out-videos/batman.mp4', './data/out-videos/batman(resized).mp4')

