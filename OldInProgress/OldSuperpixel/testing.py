import sys
import skimage
from skimage import io, filters, feature, data, segmentation
import numpy as np
import matplotlib.pyplot as plt
import cv2

image = skimage.data.coffee()
image = skimage.io.imread(fname="b.png")

io.imshow(image)
io.show()

segments = skimage.segmentation.slic(image, n_segments=400, compactness=10.0, 
										sigma=2, enforce_connectivity=True)

figure = plt.figure("Superpixels")
ax = figure.add_subplot(1, 1, 1)
ax.imshow(skimage.segmentation.mark_boundaries(skimage.util.img_as_float(
									cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		 ), segments))
plt.axis("off")
plt.show()


'''
# loop over the unique segment values
for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print("[x] inspecting segment %d",i)
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == segVal] = 255

	# show the masked region
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", cv2.bitwise_and(image, image, mask = mask))
	cv2.waitKey(0)
'''