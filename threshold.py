import os
import cv2
import time
from tqdm import tqdm
import numpy as np

INPUT_DIR = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-in"
OUTPUT_DIR = "C:\\Users\\16474\\Desktop\\lanes-utra\\threshold-out"


def create_mask(img_hsv):
    '''Create mask for red pixels using HSV color scheme'''
    sensitivity = 35
    lower_white = np.array([0,0,255-sensitivity])
    upper_white = np.array([255,sensitivity,255])
    # lower_red = np.array([161, 155, 84])
    # upper_red = np.array([179, 255, 255])
    mask = cv2.inRange(img_hsv, lower_white, upper_white)

    return mask


def get_output_img(img, mask):
    '''Convert masked image to output format'''
    output_img = img.copy()
    output_img[np.where(mask == 0)] = 0
    output_img[np.where(mask != 0)] = 255

    return output_img


def main():
    ts = []

    # iterate through input files
    for filename in tqdm(os.listdir(INPUT_DIR)):
        f = os.path.join(INPUT_DIR, filename)

        t1 = time.time()

        # convert from bgr to hsv
        img = cv2.imread(f)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # resize image
        scale_percent = 25
        width = int(img_hsv.shape[1] * scale_percent / 100)
        height = int(img_hsv.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img_hsv, dim, interpolation = cv2.INTER_AREA)

        # create white mask
        mask = create_mask(resized)

        # generate black and white output image
        output_img = get_output_img(resized, mask)

        # resize image
        scale_percent = 400
        width = int(output_img.shape[1] * scale_percent / 100)
        height = int(output_img.shape[0] * scale_percent / 100)
        dim = (width, height)
        output_img = cv2.resize(output_img, dim, interpolation = cv2.INTER_AREA)

        t2 = time.time()

        ts.append(t2 - t1)

        # save output image
        cv2.imwrite(OUTPUT_DIR + "\\" + filename, output_img)
    
    ts = [1 / t for t in ts]
    print("Average FPS: " + str(sum(ts) / len(ts)))

    import matplotlib.pyplot as plt

    plt.plot(ts)
    plt.show()


if __name__ == "__main__":
    main()
