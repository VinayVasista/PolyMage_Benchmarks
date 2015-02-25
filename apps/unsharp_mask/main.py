import ctypes
import numpy as np
import time
import cv2
import sys

sys.path.insert(0, '../')
from utils import clock, initOptionals, \
                   printLine, image_clamp

# shared library, and function
libunsharp = ctypes.cdll.LoadLibrary("./unsharp.so")
unsharp = libunsharp.pipeline_mask

# initialize the app. parameters
def initVars(image, threshold, weight, nruns, rows, cols, args):
    if len(args) < 4 :
        print "Usage:\n" + args[0] + \
              " image threshold weight [[nruns] [rows [cols]]]"
        sys.exit(1)
    else :
        image = cv2.imread(args[1], cv2.CV_LOAD_IMAGE_COLOR)
        threshold = float(args[2])
        weight = float(args[3])
        optionalArgStart = 4

        # Optional Parameters
        # default
        nruns = 6
        rows, cols, c = image.shape
        nruns, rows, cols = initOptionals(optionalArgStart, \
                                          nruns, rows, cols, args)

    return image, threshold, weight, nruns, rows, cols

#-------------------------------------------------------------------

image = ''
threshold, weight = 0.000001, 4
nruns, rows, cols = 0, 0, 0

# initialize
image, threshold, weight, nruns, rows, cols = \
    initVars(image, threshold, weight, \
             nruns, rows, cols, sys.argv)

# Values set to
print
printLine()
print 'image: \"', sys.argv[1], '\"'
print 'threshold =',threshold, 'weight =',weight
print 'nruns =',nruns,', rows =',rows,', cols =',cols

# get image roi
row_base = (image.shape[0] - rows)/2
col_base = (image.shape[1] - cols)/2
image_region = image[row_base:row_base+rows, \
                     col_base:col_base+cols]

# create ghost zones
image_ghost = np.zeros((rows+4, cols+4, 3), image_region.dtype)
image_ghost[2:rows+2, 2:cols+2, 0:3] = image_region[0:rows, 0:cols, 0:3]

# convert input image to floating point
image_f = np.float32(image_ghost) / 255.0

# move colour dimension outside
image_f_flip = np.rollaxis(image_f, 2).ravel()

# result array
res = np.empty((3, rows, cols), np.float32)

# start timer
print "-------------------------------"
startTime = time.clock()
avgTime = 0
for run in range(1, nruns+1):
    frameStart = clock()
    # Compute
    unsharp(ctypes.c_int(cols), \
            ctypes.c_int(rows), \
            ctypes.c_float(threshold), \
            ctypes.c_float(weight), \
            ctypes.c_void_p(image_f_flip.ctypes.data), \
            ctypes.c_void_p(res.ctypes.data))
    frameEnd = clock()
    frameTime = float(frameEnd) - float(frameStart)

    if run != 1:
        print frameEnd*1000 - frameStart*1000, "ms"
        avgTime += frameTime

print "-------------------------------"
print "avg time: ", (avgTime/(nruns-1))*1000, "ms"
print "-------------------------------"

# move colour dimension inside

input_image = image[row_base : row_base + rows,
                    col_base : col_base + cols,
                    0:3]

output_image = np.rollaxis(res, 0, 3)

# Display
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
