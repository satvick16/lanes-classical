import os
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

INPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-in"
OUTPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-out"

def image_prep(src):
    br = np.average(src)

    if br < 50:
        const = 1
    else:
        const = 10

    thresh = cv2.adaptiveThreshold(src,
                                   maxValue=255,
                                   adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   thresholdType=cv2.THRESH_BINARY_INV,
                                   blockSize=11,
                                   C=const)

    blobs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.zeros(thresh.shape, np.uint8)

    for blob in blobs:
        if cv2.contourArea(blob) > 100:
            cv2.drawContours(conts, [blob], 0, 255, 3)

    return conts

def main():
    ts = []

    for filename in os.listdir(INPUT):
        f = os.path.join(INPUT, filename)

        t1 = time.time()

        src = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        dst = image_prep(src)

        t2 = time.time()

        ts.append(t2 - t1)

        cv2.imwrite(OUTPUT + "\\" + filename, dst)

    fps = [1 / t for t in ts]

    plt.plot(fps)
    plt.show()

    print("Average FPS: {}".format(np.average(fps)))

if __name__ == "__main__":
    main()
