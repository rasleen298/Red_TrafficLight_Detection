import os
import cv2
import numpy as np

def detectredlight():

    count=0
    cap = cv2.VideoCapture("acc.asf")
    out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))



    while(True):
        background=0

        for i in range(30):

        
            ret, img = cap.read()
            img = cv2.resize(img, (640, 480))

        
            cimg=img
            font = cv2.FONT_HERSHEY_SIMPLEX
    
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # color range
            lower_red1 = np.array([0,100,100])
            upper_red1 = np.array([10,255,255])
            lower_red2 = np.array([160,100,100])
            upper_red2 = np.array([180,255,255])

            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            maskr = cv2.add(mask1, mask2)

            size = img.shape

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale
    

            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

            cv2.circle(img, maxLoc, 5, (255, 180, 180), 2)

    # hough circle detect
            r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                               param1=50, param2=10, minRadius=0, maxRadius=30)

            # traffic light detect
            radius = 5
            bound = 4.0 / 10
            if r_circles is not None:
                r_circles = np.uint16(np.around(r_circles))

                for i in r_circles[0, :]:
                    if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
                        continue

                    h_1, s_1 = 0.0, 0.0
                    for m in range(-radius, radius):
                        for n in range(-radius, radius):

                            if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                                continue
                            h_1 += maskr[i[1]+m, i[0]+n]
                            s_1 += 1
                    if h_1 / s_1 > 50:
                        cv2.circle(cimg, maxLoc, i[2]+10, (0, 255, 0), 2)
                        cv2.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                        cv2.putText(cimg,'RED',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

            
                        out.write(img.astype('uint8'))
                        #cv2.imwrite(f'detected results{count}.jpg', cimg)

    #cv2.imshow('detected results', cimg)
    
    # cv2.imshow('maskr', maskr)
    

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    detectredlight()


    