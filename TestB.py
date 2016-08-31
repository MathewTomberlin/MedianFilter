from PIL import Image
import numpy as np
import os.path as path

original = Image.open(str(1)+".png")
print("Image stats loaded")

width = int(original.width)
height = int(original.height)

master = np.full((height,width,3,9),255,np.uint16)
newImage = np.zeros((height,width,3),np.uint8);

def getColorValue(x,y,rgb,i):
	return master[y,x,rgb,i]

def setColorValue(x,y,rgb,i,value):
	master[y,x,rgb,i] = value

def pixelToArray(x, y, pixel, count):
	for rgb in range(0,3):
		bigVal = None;

		for i in range(0,count):
			if bigVal is None:
				if(pixel[rgb] <= getColorValue(x,y,rgb,i)):
					bigVal = getColorValue(x,y,rgb,i)			
					setColorValue(x,y,rgb,i,pixel[rgb])
			else:
				otherVal = getColorValue(x,y,rgb,i)
				setColorValue(x,y,rgb,i,bigVal)
				bigVal = otherVal

def buildMasterArray():
	for count in range(1,10):
		
		original = Image.open(str(count)+".png")
		print("Image "+str(count)+".png Loaded")

		for y in range(0,height):	
			for x in range(0,width):	
				pixel = original.getpixel((x,y))
				pixelToArray(x,y,pixel,count)

def buildMedianArrayFromMaster():
	print("Building Array of Median Values From Master")
	
	for y in range(0,height):
		for x in range(0,width):
			for rgb in range(0,3):
				val = round(((master[y,x,rgb,4]+master[y,x,rgb,5])/2))
				newImage[y,x,rgb] = val

def saveImage(image):
	n = 0
	saved = False

	while path.exists("PostProcess"+str(n)+".png") is True:
		n+=1
	image.save("PostProcess"+str(n)+".png");
	print("New Image Saved as PostProcess"+str(n)+".png")


if __name__ == '__main__':
	if original is not None:
		buildMasterArray()
		
		buildMedianArrayFromMaster()

		image = Image.fromarray(newImage,'RGB');

		saveImage(image)
