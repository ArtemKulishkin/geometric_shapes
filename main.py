import cv2
import numpy as np
import math

def find_contours(img, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, color[0], color[1])
    contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

img = cv2.imread("pool_two_bins.jpg")
if img.any() == None:
    print("Не найдена картинка")
    exit()
drawing = img.copy()
color = (
          (30, 80, 0),
          (70, 200, 255)  
        )
contours = find_contours(img, color)

if contours:
    for cnt in contours:
        if cv2.contourArea(cnt) > 50:
            contour_area = cv2.contourArea(cnt)
            print("Площадь контура:", contour_area)

            cv2.drawContours(drawing, [cnt], 0, (255, 255, 255), 2)
            (circle_x, circle_y), circle_radius = cv2.minEnclosingCircle(cnt)
            circle_area = math.pi * circle_radius**2
            print("Площадь окружности:", circle_area)
            

            rectangle = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rectangle)
            box = np.int0(box)
            rectangle_area = cv2.contourArea(box)
            print("Площадь прямоугольника:", rectangle_area)
           
            rect_w, rect_h = rectangle[1][0], rectangle[1][1]
            aspect_ratio = max(rect_w, rect_h) / min(rect_w, rect_h)

            try:
                triangle = cv2.minEnclosingTriangle(cnt)[1]
                triangle = np.int0(triangle)
                triangle_area = cv2.contourArea(triangle)
                
            except:
                triangle_area = 0

            print("Площадь треугольника:", triangle_area)
            
            print()

            shapes_areas = {
                'circle': circle_area,
                'rectangle' if aspect_ratio > 1.25 else 'square': rectangle_area,
                'triangle': triangle_area
            }

            diffs = {
                name: abs(contour_area - shapes_areas[name]) for name in shapes_areas
            }
            shape_name = min(diffs, key=diffs.get)
            if shape_name == "triangle":
                cv2.drawContours(drawing, [triangle], -1, (100, 255, 155), 2)
            elif shape_name == "rectangle" or shape_name == "square":
                cv2.drawContours(drawing, [box], 0, (0, 150, 255), 2)
            else:
                cv2.circle(drawing, (int(circle_x), int(circle_y)), int(circle_radius), (255, 255, 0), 2)
            
            moments = cv2.moments(cnt)

            try:
                x = int(moments['m10']/moments['m00'])
                y = int(moments['m01']/moments['m00'])
                cv2.circle(drawing, (x, y), 4, (0, 100, 255), -1, cv2.LINE_AA)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(drawing, shape_name, (x-40, y+31), font, 1, (0, 0, 0), 4, cv2.LINE_AA)
                cv2.putText(drawing, shape_name, (x-41, y+30), font, 1, (255, 255, 255), 4, cv2.LINE_AA)
            except ZeroDivisionError:
                pass
            print()
            
cv2.imshow("drawing", drawing)
cv2.waitKey(0)