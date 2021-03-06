import imutils
import cv2
#redlower(HueLower,SaturationLower,ValueLower)
redLower=(157,93,203)
redUpper=(179,255,255)
camera=cv2.VideoCapture(0)
while True:
    (grabbed,frame)=camera.read()
    frame=imutils.resize(frame,width=600)
    blurred=cv2.GaussianBlur(frame,(11,11),0)
    hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(hsv,redLower,redUpper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
#area and presence of the color of the object.
    cnts=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] 
    center=None
    if len(cnts)>0:#To draw the minimum enclosure circle and midpoint
        c=max(cnts,key=cv2.contourArea)#Maximum Contour Area
        ((x,y), radius)=cv2.minEnclosingCircle(c)#Obtain Center point and Radius
        M=cv2.moments(c)#radius of c
        center=(int(M["m10"]/M["m00"]), int (M["m01"]/ M["m00"]))
        if radius>10:
            cv2.circle(frame,(int(x), int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)
            print(center[0],radius)
    #application Part

            if radius > 250:
                       print("stop")
            else:#Use the centriod to choose right or left
                if (center[0]<150):
                    print("Left")
                elif (center[0]>450):
                    print("Right")
                elif (radius<250):#use circle to choose front or far
                    print("Front")
                else:
                    print("Stop")
    
    cv2.imshow("Frame",frame)
    key=cv2.waitKey(1) & 0xFF
    if key==ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
