import sys
import skimage
from skimage import io, filters, feature

#python .\ImgToEdges.py b.png 2.5 .01 .15
#python .\ImgToEdges.py b.png 2.4 .04 .17  <== This is the one

# read command-line arguments
filename = sys.argv[1]

sigma = 2.4
low_threshold = 0.04
high_threshold = 0.17

'''
sigma = float(sys.argv[2])
low_threshold = float(sys.argv[3])
high_threshold = float(sys.argv[4])
'''

# load the original image as grayscale
image = skimage.io.imread(fname=filename, as_gray=True)


#Perform Canny edge detection on the image
image = skimage.feature.canny(
    image=image,
    sigma=sigma,
    low_threshold=low_threshold,
    high_threshold=high_threshold,
)
'''

image = filters.gaussian(image)
image = filters.sobel(image)
image = skimage.feature.CENSURE(image)  #<-- Doesn't exist, just for reference
'''

#from scipy import ndimage
#image = ndimage.binary_fill_holes(image)
#Save to disk (Image is boolean, T for edge, F for no edge... F = 0, T = 255)
#io.imsave(fname='edges.png', arr=skimage.img_as_bool(image))
io.imsave(fname='edges.png', arr=skimage.img_as_int(image))

#Display edges
io.imshow(image)
io.show()

