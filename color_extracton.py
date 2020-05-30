import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Reading the image 
img = cv2.imread("color.jpg")

clicked = False
name = []
bgr = []

#Reading csv file 
color_col = ["color","color_name","hex","R","G","B"]
df = pd.read_csv('colors.csv', names=color_col, header=None)
Red = df["R"]
Green = df["G"]
Blue = df["B"]
color_name = df["color_name"]

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R- int(Red[i])) + abs(G- int(Green[i]))+ abs(B- int(Blue[i]))
        if(d<=minimum):
            minimum = d
            cname = color_name[i]
    name.append(cname)
    return cname

#function to get x,y coordinates of mouse left click
def position(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,clicked
        clicked = True
        b = int(img[y,x,0])
        g = int(img[y,x,1])
        r = int(img[y,x,2])
        bgr.append([b,g,r])
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',position)

while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        cv2.rectangle(img,(20,20), (400,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b)

        if(r+g+b>=500):
            cv2.putText(img, text,(50,50),3,0.8,(0,0,0),2,cv2.LINE_AA)
        else:
            cv2.putText(img, text,(50,50),3,0.8,(255,255,255),2,cv2.LINE_AA) 
        clicked=False

    #Press 'esc' key to exit 
    if cv2.waitKey(20) ==27:
        break

#for plotting the colors
colors = []
for i in range(len(bgr)):
    mycolor = np.zeros((5,5,3), np.uint8)
    mycolor[:] = [bgr[i][2],bgr[i][1],bgr[i][0]]
    colors.append(mycolor)   

fig = plt.figure()
for i in range(len(colors)):
    if len(colors) <= 3:
        ax = fig.add_subplot(2, 2, i+1)
    elif len(colors) == 5:
        ax = fig.add_subplot(3, 3, i+1)
    else:
        ax = fig.add_subplot((len(colors))/2, (len(colors))/2, i+1)
    ax.imshow(colors[i])
    ax.set_xticks([]) 
    ax.set_yticks([]) 
    ax.title.set_text(name[i])

#fig.suptitle('Extracted Colors') 

plt.tight_layout()
plt.show()   
cv2.destroyAllWindows()