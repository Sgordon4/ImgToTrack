from PyQt5 import QtCore, QtGui, QtWidgets
from skimage import data, viewer
image = data.coins()
viewer = viewer.ImageViewer(image) 
viewer.show()               