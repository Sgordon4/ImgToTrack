import sys
import skimage
from skimage import io, filters, feature


#Load the edges image
edges = skimage.io.imread(fname="edges.png")

#Apply the closing operation (Dilation then erosion)
#skimage.morphology.area_closing(edges, 64, 1)


for x in range (1):
	edges = skimage.morphology.binary_dilation(edges)
	

for x in range (0):
	edges = skimage.morphology.binary_erosion(edges)
	
#edges = skimage.measure.find_contours(edges, 0.8)
	



#Save to disk (Image is boolean, T for edge, F for no edge... F = 0, T = 255)
io.imsave(fname='closed.png', arr=skimage.img_as_bool(edges))

#Display edges
#io.imshow(edges)
#io.show()
io.imshow(edges)
io.show()
