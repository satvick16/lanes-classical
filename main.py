import os
import cv2
import numpy as np

INPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\input"
OUTPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\output"


def image_prep(src):
    '''Denoise image, apply adaptive thresholding and find Canny edges.'''

    # denoise image
    thing = src.copy()
    src = cv2.fastNlMeansDenoising(thing, src, h=20)

    # cv2.imshow("test", src)
    # cv2.waitKey()

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
                                   thresholdType=cv2.THRESH_BINARY,
                                   blockSize=11,
                                   C=const)

    src = thresh.copy()

    # cv2.imshow("test", src)
    # cv2.waitKey()

    # use Canny edge detector
    dst = cv2.Canny(src,
                    threshold1=900,
                    threshold2=1000,
                    edges=None,
                    apertureSize=3)

    # cv2.imshow("test", dst)
    # cv2.waitKey()

    return dst


def main():
    # iterate through input files
    for filename in os.listdir(INPUT):
        f = os.path.join(INPUT, filename)

        src = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        shape = src.shape

        # denoise, threshold, canny
        dst = image_prep(src)

        # save output image
        cv2.imwrite(OUTPUT + "\\" + filename, dst)


if __name__ == "__main__":
    main()
