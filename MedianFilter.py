from PIL import Image
import numpy as np
import os
import os.path
import math
#Name: MedianFilter
#Author: Mathew Tomberlin
#Date:9/7/2016
#Abstract: This class 

#Check if the OriginalImages folder exists in the program path
if(os.path.exists("OriginalImages")):
	#Get the number of images in the OriginalImages folder
	numberOfImages = len(os.listdir("OriginalImages"))
	if(numberOfImages > 0):
		#Open the first image
		original = Image.open("OriginalImages/"+str(1)+".png")
		print("Image stats loaded")
	else:
		print("'OriginalImages' directory must contain at least one png image")
	
else:
	print("No directory names 'OriginalImages' found. You must have a directory named 'OriginalImages' in your working directory")

#Get the width and the height of the first picture
width = int(original.width)
height = int(original.height)

#Fill the master array with 255
#Fill the new image array with 0s
master = np.full((height,width,3,numberOfImages),255,np.uint16)
newImage = np.zeros((height,width,3),np.uint8);

#Return the 8-bit value of the rgb color [0=r,1=g,2=b] at pixel (x,y) for image i from the master array
def getColorValue(x,y,rgb,i):
	return master[y,x,rgb,i]

#Set the 8-bit value of the rgb color [r=0,g=1,b=2] at pixel (x,y) for image i in the master array
def setColorValue(x,y,rgb,i,value):
	master[y,x,rgb,i] = value

#For each rgb color [r=0,g=1,b=2] in the pixel at (x,y), start at 0 and count up through the current document we're processing

#If the rgb value of the pixel at (x,y) is less than or equal to the value stored for that rgb color at pixel (x,y) at i, then
#store the previous value and set the value stored to the pixel rgb value

#Once the above occurs, get the value at the next array slot and move the previous value to the next slot to move the values up
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
#For each image in the 'OriginalImages' folder, try to load the image. If it is loaded, get each pixel in the image and add it to the
#master pixel array using the pixelToArray() method. That method inserts each color value of the pixel in to the master array in order
def buildMasterArray():
	for count in range(1,numberOfImages+1):
		try:
			original = Image.open("OriginalImages/"+str(count)+".png")
			print("Image "+str(count)+".png Loaded")
		except:
			print("Image "+str(count)+".png not found in directory 'OriginalImages'. Your images must be named '#.png', starting with 1")
			return -1

		for y in range(0,height):	
			for x in range(0,width):	
				pixel = original.getpixel((x,y))
				pixelToArray(x,y,pixel,count)

#For each rgb color in each pixel: 
#If the number of images is even, add the middle two image's rgb color value together and divide by two (Find the median)
#If the number of images is odd, the middle image's rgb color value is divided by two (Find the median)
def buildMedianArrayFromMaster():
	print("Building Array of Median Values From Master")
	
	for y in range(0,height):
		for x in range(0,width):
			for rgb in range(0,3):
				if (numberOfImages % 2) is 1:
					val = ((master[y,x,rgb,int(numberOfImages/2)])+(master[y,x,rgb,int(numberOfImages/2)+1]))/2
					newImage[y,x,rgb] = val
				else:
					val = master[y,x,rgb,int(numberOfImages/2)]
					newImage[y,x,rgb] = val

#Increments an iterator if the potential filename already exists
#Then saves the file once a suitable name is found
def saveImage(image):
	n = 0

	while os.path.exists("PostProcess"+str(n)+".png") is True:
		n+=1
	image.save("PostProcess"+str(n)+".png");
	print("New Image Saved as PostProcess"+str(n)+".png")


if __name__ == '__main__':
	if original is not None:
		if(buildMasterArray() is None):
		
			buildMedianArrayFromMaster()

			image = Image.fromarray(newImage,'RGB');

			saveImage(image)
	else:
		print("Quitting with error")
