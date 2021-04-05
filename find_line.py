import numpy as np
import glob
import cv2

class Lane:
    def __init__(self):
        self.fit_coef = 0

def calibrate_camera(images, grid_size=(9, 6)):
    """
    Calibrate camera parameters using images of 
    chesseboard

    :param images list : list of image path
    :param grid_size tuple: size of grid
    """
    if len(images) < 10:
        print('Not enough images for clibration!')
        return
    gw, gh = grid_size
    objp = np.zeros((gw*gh,3), np.float32)
    objp[:,:2] = np.mgrid[0:gw, 0:gh].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.

    # Step through the list and search for chessboard corners
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (gw,gh), None)
        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
    img_size = gray.shape
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, img_size, 1, img_size)
    return mtx, dist, newcameramtx, roi

def undistort_image(img, mtx, dist, newcameramtx=None, roi=None):
    """
    undistort image

    :param img image: image to be undistort
    :param mtx matrix: matrix for undisortion
    :param dist matrix : dist coeffients
    :param newcameramtx matrix: new camera matirx
    :param roi tuple: roi of valid pixels  
    """
    if (newcameramtx != None) and (roi != None):
        x,y,w,h = roi
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        dst = dst[y:y+h, x:x+w]
    else:
        dst = cv2.undistort(img, mtx, dist, None, mtx)
    return dst

 
if __name__ == '__main__':
    # 1. Camera Calibration
    cali_path = 'camera_cal/*.jpg'
    mtx, dist, newcameramtx, roi = calibrate_camera(glob.glob(cali_path)) 
    # 2. Camera Undistortion
    # 3. Filter Image
    # 4. Find Lane 
    # 5. Sanity Check
    # 6. Track Lane
    # 7. Draw Lane
    print('a')
