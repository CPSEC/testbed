import os
from cv2 import cv2


def get_images_by_dir(dir):
    """
    """
    img_names = os.listdir(dir)
    img_paths = [dir+'/'+img_name for img_name in img_names]
    imgs = [cv2.imread(path) for path in img_paths]
    return imgs


def get_images_by_dir_name(dir, name):
    """
    """
    pass
