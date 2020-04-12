import utils
from camera_calibration import *
from threasholding import *
from perspective_transform import *
from detect_lane import *
from cal_curv_pos import *
from show import *

if __name__ == '__main__':
    # test chessboard
    cal_imgs = utils.get_images_by_dir(
        os.path.join(os.getcwd(), 'img\\chessboard'))
    # cv2.imshow('img',cal_imgs[0])
    # cv2.waitKey(0)
    object_points, img_points = calibrate(cal_imgs, grid=(9, 6))
    # print(len(cal_imgs), object_points, img_points)
    test_imgs = utils.get_images_by_dir(os.path.join(os.getcwd(), 'img\\test'))
    test_imgs = [test_imgs[0]]
    undistorted_imgs = []
    for img in test_imgs:
        #img = cal_undistort(img, object_points, img_points)
        undistorted_imgs.append(img)
    # cv2.imshow("", undistorted_imgs[0])
    # cv2.waitKey(0)

    # tmp = undistorted_imgs[0]
    # tmp = abs_sobel_thresh(tmp, orient='x', thresh_min=10, thresh_max=230)
    # tmp = mag_thresh(tmp, sobel_kernel=9, mag_thresh=(30, 150))
    # tmp=dir_threshold(img,sobel_kernel=3,thresh=(0.7,1.3))
    # tmp=hls_select(tmp,channel='s',thresh=(180,255))
    # tmp=lab_select(tmp,(180,255))
    # tmp=luv_select(tmp,thresh=(225,255))
    # cv2.imshow("", tmp)
    # cv2.waitKey(0)

    thresholded_imgs = []
    for img in undistorted_imgs:
        img = combine_threshold(img)
        thresholded_imgs.append(img)
    # cv2.imshow("", thresholded_imgs[0])
    # cv2.waitKey(0)

    tmp = thresholded_imgs[0]
    M, Minv = get_M_Minv()
    tmp = cv2.warpPerspective(tmp, M, tmp.shape[1::-1], flags=cv2.INTER_LINEAR)
    # cv2.imshow("",tmp)
    # cv2.waitKey(0)

    left_fit, right_fit, left_lane_inds, right_lane_inds = find_line(tmp)
    print(left_fit, right_fit, left_lane_inds, right_lane_inds)

    undist = undistorted_imgs[0]
    r = draw_area(undist, tmp, Minv, left_fit, right_fit)
    # cv2.imshow("",r)
    # cv2.waitKey(0)

    curvature, distance_from_center = calculate_curv_and_pos(
        tmp, left_fit, right_fit)
    r = draw_values(r, curvature, distance_from_center)
    cv2.imshow("", r)
    cv2.waitKey(0)
