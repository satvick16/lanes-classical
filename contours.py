import os
import cv2
import time
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

INPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-in"
OUTPUT = "C:\\Users\\16474\\Desktop\\lanes-utra\\contours-out"

def lanes(src):
    thresh = cv2.adaptiveThreshold(src,
                                   maxValue=255,
                                   adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   thresholdType=cv2.THRESH_BINARY_INV,
                                   blockSize=11,
                                   C=10)

    blobs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.zeros(thresh.shape, np.uint8)

    for blob in blobs:
        if cv2.contourArea(blob) > 100:
            cv2.drawContours(conts, [blob], 0, 255, 3)

    return conts

def main():
    ts = []

    for filename in tqdm(os.listdir(INPUT)):
        # if not (filename.endswith(".png") and int(filename[:-4]) > 150 and int(filename[:-4]) < 300):
        #     continue

        f = os.path.join(INPUT, filename)

        t1 = time.time()

        src = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        dst = lanes(src)

        t2 = time.time()

        ts.append(t2 - t1)

        cv2.imwrite(OUTPUT + "\\" + filename, dst)

    fps = [1 / t for t in ts]

    plt.plot(fps)
    plt.show()

    print("Average FPS: {}".format(np.average(fps)))

if __name__ == "__main__":
    main()
