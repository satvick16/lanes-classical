import os
import cv2
import numpy as np
import time

from PIL import Image, ImageFilter

INPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\input"
OUTPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\output"

def contours(img):
    # get blobs in image
    # get angle of each blob
    blobs, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # create new image to draw contours on
    img = np.zeros(img.shape, np.uint8)

    for blob in blobs:
        # contour = blob[0]

        # print(blob)

        # if blobs are bigger than a 3x3 square
        if cv2.contourArea(blob) > 100:
            # draw contours on image
            cv2.drawContours(img, [blob], 0, 255, 3)
            # print(blob[:,0,0])
    
    return img

def image_prep(src):
    '''Denoise image, apply adaptive thresholding and find Canny edges.'''

    # denoise image
    # thing = src.copy()
    # src = cv2.fastNlMeansDenoising(thing, src, h=20)

    # cv2.imshow("test", src)
    # cv2.waitKey()

    # adjust "C" for adaptive threshold based on image brightness
    # br = np.average(src)

    # if br < 50:
    #     const = 1
    # else:
    #     const = 10

    # adaptive gaussian threshold
    thresh = cv2.adaptiveThreshold(src,
                                   maxValue=255,
                                   adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   thresholdType=cv2.THRESH_BINARY_INV,
                                   blockSize=11,
                                   C=10)

    conts = contours(thresh)

    # src = thresh.copy()

    # cv2.imshow("test", src)
    # cv2.waitKey()

    # use Canny edge detector
    # dst = cv2.Canny(src,
    #                 threshold1=900,
    #                 threshold2=1000,
    #                 edges=None,
    #                 apertureSize=7)

    dst = conts

    # cv2.imshow("test", dst)
    # cv2.waitKey()

    return dst


def main():
    ts = []

    # iterate through input files
    for filename in os.listdir(INPUT):
        f = os.path.join(INPUT, filename)

        t1 = time.time()

        _ = Image.open(f)
        blur = _.filter(ImageFilter.BLUR)

        src = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        dst = image_prep(src)

        t2 = time.time()

        ts.append(t2 - t1)

        # save output image
        cv2.imwrite(OUTPUT + "\\" + filename, dst)

    # print(sum(ts) / len(ts))
    print(f"Average framerate: {1 / (sum(ts) / len(ts))} fps")


if __name__ == "__main__":
    main()
