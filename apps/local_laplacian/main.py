import ctypes
import numpy as np
import time
import cv2
import sys

sys.path.insert(0, '../')
from utils import clock, initOptionals, \
                   printLine, image_clamp

# shared library, and function
libll = ctypes.cdll.LoadLibrary("./laplacian.so")
laplacian = libll.pipeline_laplacian

# initialize the app. parameters
def initVars(image, alpha, beta, nruns, rows, cols, args):
    if len(args) < 4 :
        print "Usage:\n" + args[0] + \
              " image alpha beta [[nruns] [rows [cols]]]"
        sys.exit(1)
    else :
        image = cv2.imread(args[1], cv2.CV_LOAD_IMAGE_COLOR)
        alpha = float(args[2])
        beta = float(args[3])
        optionalArgStart = 4

        # Optional Parameters
        # default
        nruns = 6
        rows, cols = 2560, 1536
        nruns, rows, cols = initOptionals(optionalArgStart, \
                                          nruns, rows, cols, args)

    return image, alpha, beta, nruns, rows, cols

#-------------------------------------------------------------------

L = 8
levels = 8
image = ''
alpha, beta = 0.0, 0.0
nruns, rows, cols = 0, 0, 0

# initialize
image, alpha, beta, nruns, rows, cols = \
    initVars(image, alpha, beta, \
             nruns, rows, cols, sys.argv)

# Values set to
printLine()
print 'image: \"', sys.argv[1], '\"'
print 'alpha =',alpha,', beta =',beta
print 'nruns =',nruns,', rows =',rows,', cols =',cols

if rows != 2560 or cols != 1536:
    print "Please use 1536x2560 image size"
    sys.exit(0)

alpha /= (levels-1)

R = image.shape[0]
C = image.shape[1]

# get image roi
row_base = (R - rows)/2
col_base = (C - cols)/2
image_region = image[row_base:row_base+rows, \
                     col_base:col_base+cols]

# create ghost zone and copy image roi as ushort
image_ghost = np.zeros((rows+4, cols+4, 3), np.uint16)
image_ghost[2:rows+2, 2:cols+2, 0:3] = \
    np.array(image_region * 256, np.uint16)

# move colour dimension outside
image_flip = np.rollaxis(image_ghost, 2)
image_flip = image_flip.ravel()

# result array
res = np.zeros((3, rows, cols), np.uint16)

# start timer
print "-------------------------------"
startTime = time.clock()
avgTime = 0
for run in range(1, nruns+1):
    frameStart = clock()
    # Compute
    laplacian(ctypes.c_int(cols), ctypes.c_int(rows), \
             ctypes.c_float(alpha), ctypes.c_float(beta), \
             ctypes.c_void_p(image_flip.ctypes.data), \
             ctypes.c_void_p(res.ctypes.data)
            )
    frameEnd = clock()
    frameTime = float(frameEnd) - float(frameStart)

    if run != 1:
        print frameEnd*1000 - frameStart*1000, "ms"
        avgTime += frameTime

print "-------------------------------"
print "avg time: ", (avgTime/(nruns-1))*1000, "ms"
print "-------------------------------"

# Display

# reshape and move colour dimension inside
image_ghost = image_flip.reshape(3,rows+4,cols+4)
input_ghost = np.rollaxis(image_ghost, 0, 3)
input_image = input_ghost[2:rows+2, 2:cols+2]

output_image = np.rollaxis(res, 0, 3)

cv2.namedWindow("input", cv2.WINDOW_NORMAL)
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
ch = 0xFF
while [ ch != ord('q') ]:
    ch = 0xFF & cv2.waitKey(1)
    cv2.imshow("input", input_image)
    cv2.imshow("output", output_image)
    if ch == ord('q'):
        break

cv2.destroyAllWindows()
