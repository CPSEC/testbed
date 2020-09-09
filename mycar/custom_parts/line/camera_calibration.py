import os
import numpy as np
from cv2 import cv2
import utils


def calibrate(images, grid=(9, 6)):
    """
    Parameter:
        images: a image
        grid: 
    Return:
        object_points: 
        img_points:
    """
    object_points = []
    img_points = []
    for img in images:
        object_point = np.zeros((grid[0]*grid[1], 3), np.float32)
        object_point[:, :2] = np.mgrid[0:grid[0], 0:grid[1]].T.reshape(-1, 2)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, grid, None)
        if ret:
            object_points.append(object_point)
            img_points.append(corners)
    return object_points, img_points


def cal_undistort(img, obj_points, img_points):
    """
    Parameter:
        img:
        obj_points:
        img_points:
    Return:
        dst:
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, img.shape[1::-1], None, None)
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    return dst
