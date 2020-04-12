from cv2 import cv2
import numpy as np


def get_M_Minv():
    """
    Transfer thresholded img to view from above
    """
    # src = np.float32([[(203, 720), (585, 460), (695, 460), (1127, 720)]])
    # dst = np.float32([[(320, 720), (320, 0), (960, 0), (960, 720)]])
    src = np.float32([[(20, 120), (70, 80), (90, 80), (140, 120)]])
    dst = np.float32([[(20, 120), (40, 0), (100, 0), (140, 120)]])
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    return M, Minv
