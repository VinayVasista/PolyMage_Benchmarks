import ctypes
import numpy as np
import time
import cv2
import sys

sys.path.insert(0, '../')
from utils import clock, initOptionals, \
                   printLine, image_clamp

# shared library, and function
libharris = ctypes.cdll.LoadLibrary("./harris.so")
harris = libharris.pipeline_harris

# initialize the app. parameters
def initVars(image, nruns, rows, cols, args):
    if len(args) < 2 :
        print "Usage:\n" + sys.argv[0] + \
              " image [[nruns] [rows [cols]]]"
        sys.exit(1)
    else :
        image = cv2.imread(args[1], cv2.CV_LOAD_IMAGE_COLOR)
        optionalArgStart = 2

        # Optional Parameters
        # default
        nruns = 6
        rows, cols, c = image.shape
        nruns, rows, cols = initOptionals(optionalArgStart, \
                                          nruns, rows, cols, sys.argv)

    return image, nruns, rows, cols

#----------------------------------------------------------------------

image = ''
nruns, rows, cols = 0, 0, 0

# initialize
image, nruns, rows, cols = initVars(\
    image, nruns, rows, cols, \
    sys.argv)

# Values set to
print "-------------------------------"
print 'image: \"', sys.argv[1], '\"'
print 'nruns =', nruns,', rows =', rows,', cols =', cols
print "-------------------------------"

# get image roi
row_base = (image.shape[0] - rows)/2
col_base = (image.shape[1] - cols)/2
image_region = image[row_base:row_base+rows, col_base:col_base+cols]

# convert input image to grayscale floating point
gray = cv2.cvtColor(image_region, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray) / 255.0

# result array
imgShow = image_region
res = np.empty((rows, cols), np.float32)

# start timer
startTime = time.clock()
avgTime = 0
for run in range(1, nruns+1):
    frameStart = clock()
    # Compute
    harris(ctypes.c_int(cols-2), \
           ctypes.c_int(rows-2), \
           ctypes.c_void_p(gray.ctypes.data), \
           ctypes.c_void_p(res.ctypes.data))
    frameEnd = clock()
    frameTime = float(frameEnd) - float(frameStart)

    if run != 1:
        print frameEnd*1000 - frameStart*1000, "ms"
        avgTime += frameTime

print "-------------------------------"
print "avg time: ", (avgTime/(nruns-1))*1000, "ms"
print "-------------------------------"

print
print "Displaying corner map with increased intensity"
print
# Display
cv2.namedWindow("input", cv2.WINDOW_NORMAL)
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
ch = 0xFF
while [ ch != ord('q') ]:
    ch = 0xFF & cv2.waitKey(1)
    cv2.imshow("input", gray)
    cv2.imshow("output", res*65535.0)
    # increase intensity in order to view 
    # the corner map

    if ch == ord('q'):
        break

cv2.destroyAllWindows()
