import numpy as np
from cv2 import cv2


def draw_area(undist, binary_warped, Minv, left_fit, right_fit):
    """
    Parameter:
        undist:
        binary_wraped:
        Minv:
        left_fit:
        right_fit:
    Return:
        result:
    """
    # Generate x and y values for plotting
    ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array(
        [np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = cv2.warpPerspective(
        color_warp, Minv, (undist.shape[1], undist.shape[0]))
    # Combine the result with the original image
    result = cv2.addWeighted(undist, 1, newwarp, 0.3, 0)
    return result


def draw_values(img, curvature, distance_from_center):
    """
    Parameter:
        img:
        curvature:
        distance_from_center:
    Return:
        img:
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    radius_text = "Radius of Curvature: %sm" % (round(curvature))

    if distance_from_center > 0:
        pos_flag = 'right'
    else:
        pos_flag = 'left'

    cv2.putText(img, radius_text, (0, 10), font, 0.4, (255, 255, 255), 1)
    # cv2.putText(img, radius_text, (100, 100), font, 1, (255, 255, 255), 2)
    center_text = " %.3fm %s of center" % (
        abs(distance_from_center), pos_flag)
    cv2.putText(img, center_text, (0, 20), font, 0.4, (255, 255, 255), 1)
    # cv2.putText(img, center_text, (100, 150), font, 1, (255, 255, 255), 2)
    return img
