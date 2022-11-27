import os
import cv2
import numpy as np

thing = []

INPUT_DIR = "C:\\Users\\16474\\Desktop\\lanes-utra\\lanes-big-in"
OUTPUT_DIR = "C:\\Users\\16474\\Desktop\\lanes-utra\\threshold-out"

ACTUAL_OUTPUTS = "C:\\Users\\16474\\Desktop\\lanes-utra\\actual-outputs"

# iterate through threshold-out files
for filename in os.listdir(OUTPUT_DIR):
    f1 = os.path.join(INPUT_DIR, filename)
    f2 = os.path.join(OUTPUT_DIR, filename)

    img1 = cv2.imread(f1)
    img2 = cv2.imread(f2)
    
    Hori = np.concatenate((img1, img2), axis=1)
    
    # cv2.imshow('HORIZONTAL', Hori)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cv2.imwrite(os.path.join(ACTUAL_OUTPUTS, filename), Hori)