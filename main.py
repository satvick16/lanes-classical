import os
import cv2
import numpy as np
import time

from PIL import Image, ImageFilter

INPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-in"
OUTPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-out"

def contours(img):
    blobs, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = np.zeros(img.shape, np.uint8)

    for blob in blobs:
        if cv2.contourArea(blob) > 100:
            cv2.drawContours(img, [blob], 0, 255, 3)
    
    return img

def image_prep(src):
    '''Denoise image, apply adaptive thresholding and find Canny edges.'''

    # denoise image
    # thing = src.copy()
    # src = cv2.fastNlMeansDenoising(thing, src, h=20)

    # adjust "C" for adaptive threshold based on image brightness
    br = np.average(src)

    if br < 50:
        const = 1
    else:
        const = 10

    # adaptive gaussian threshold
    thresh = cv2.adaptiveThreshold(src,
                                   maxValue=255,
                                   adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   thresholdType=cv2.THRESH_BINARY_INV,
                                   blockSize=11,
                                   C=const)

    conts = contours(thresh)

    # src = thresh.copy()

    # cv2.imshow("test", src)
    # cv2.waitKey()

    # use Canny edge detector
    # conts = cv2.Canny(conts,
    #                 threshold1=900,
    #                 threshold2=1000,
    #                 edges=None,
    #                 apertureSize=7)

    # cv2.imshow("test", dst)
    # cv2.waitKey()

    return conts


def main():
    ts = []

    # iterate through input files
    for filename in os.listdir(INPUT):
        f = os.path.join(INPUT, filename)

        t1 = time.time()

        # _ = Image.open(f)
        # blur = _.filter(ImageFilter.BLUR)

        src = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        dst = image_prep(src)

        t2 = time.time()

        ts.append(t2 - t1)

        # save output image
        cv2.imwrite(OUTPUT + "\\" + filename, dst)

    fps = [1 / t for t in ts]

    import matplotlib.pyplot as plt

    plt.plot(fps)
    plt.show()

    print("Average FPS: {}".format(np.average(fps)))


if __name__ == "__main__":
    main()
