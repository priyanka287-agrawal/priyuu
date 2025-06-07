
import cv2
import pickle
import cvzone
import numpy as np


# Read the image

width,height=50,20   #110-60,230-210
try:
    with open('CarParkPos', 'rb') as f:  # file name,the read permission,f is file
      posList=pickle.load(f)   #storing the previous clicks and boxes
except:
      posList= []

def click(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:  #which means we dont want unwanted clicks on other part of area so we restrict the positions
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
                break
    with open('CarParkPos','wb')as f:  #file name,write permission,f is file
        pickle.dump(posList,f)
def checkParkingSpace(imgPro,img):
    freeSpaces = 0
    img_height, img_width = img.shape[:2]

    for pos in posList:
        x, y = pos
        if y + height <= img_height and x + width <= img_width:
            imgCrop = imgPro[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)
            if count < 400:
                color = (0, 255, 0)
                text = f"Free: {count}"
                freeSpaces += 1
            else:
                color = (0, 0, 255)
                text = f"Taken: {count}"

            cv2.rectangle(img, (x, y), (x + width, y + height), color, 2)
            cvzone.putTextRect(img, text, (x, y - 5), scale=0.8, thickness=1, colorR=color, offset=5)

    # === Display Summary ===
    cvzone.putTextRect(img, f"Free: {freeSpaces}/{len(posList)}", (50, 50), scale=2, thickness=3, colorR=(0, 200, 0))
    # looking at pixelcount convert it to binary image and playing corners and edges
# Draw rectangle once
while True:
    img = cv2.imread('car.png')
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,35,16)
    kernel=np.ones((3,3),np.uint8)
    imgDilate=cv2.dilate(imgThreshold,kernel,iterations=1)
    checkParkingSpace(imgDilate,img)
    #for pos in posList

# Display the image in a loop
    cv2.imshow("Image", img)
    cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThresh", imgThreshold)
    cv2.imshow("ImageDilay",imgDilate)
    cv2.setMouseCallback("Image",click)
    cv2.waitKey(1)

