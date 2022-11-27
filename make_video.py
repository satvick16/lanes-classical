from PIL import Image
import os
import cv2
import numpy as np

ACTUAL_OUTPUTS = "C:\\Users\\16474\\Desktop\\lanes-utra\\actual-outputs"

def write_video(file_path, frames, fps):
    """
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """

    w, h = frames[0].size
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(file_path, fourcc, fps, (w, h))

    for frame in frames:
        # im_np = np.asarray(im_pil)
        writer.write(np.asarray(frame))

    writer.release()

imgs = []

# iterate through actual-outputs directory
for filename in os.listdir(ACTUAL_OUTPUTS):
    f = os.path.join(ACTUAL_OUTPUTS, filename)
    img = cv2.imread(f)

    # convert to PIL.Image
    im_pil = Image.fromarray(img)

    imgs.append(im_pil)

write_video("C:\\Users\\16474\\Desktop\\lanes-utra\\demo.mp4", imgs, 2)