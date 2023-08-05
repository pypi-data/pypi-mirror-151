import cv2
import numpy as np
import sys
from datetime import datetime
import os
# import pytesseract

class ObjectDetector:
    def __init__(self,weights,cfg,classes):
        self.net = cv2.dnn.readNet(weights,cfg)
        self.classes = classes
        self.layer_names = self.net.getLayerNames()
        try:
            self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        except IndexError:
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(classes), 3))

    def detect_object(self,img,label=True,detected_only=False):
        try:
            self.img = cv2.imread(img)
        except:
            if isinstance(img, np.ndarray):
                self.img = img
        # self.img = cv2.resize(self.img, None, fx=0.4, fy=0.4)
        # print(img)
        height, width, channels = self.img.shape
        blob = cv2.dnn.blobFromImage(self.img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    try:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                    except OverflowError:
                        pass

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)            

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # print(indexes)
        # print(boxes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                color = self.colors[0]
                cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
                print(str(self.classes[class_ids[i]]))
                self.licence = self.img[y:y+h,x:x+w]
                if label:
                    label = str(self.classes[class_ids[i]])
                    cv2.putText(self.img, label, (x, y + 30), font, 3, color, 3)
                if detected_only:
                    return self.img
        if not detected_only:
            return self.img

    # def extract_text(self):
    #     text = pytesseract.image_to_string(self.licence)
    #     return text.strip()

class ExtractImages:
    def __init__(self,path,op='Output',skip=30):
        self.cap = cv2.VideoCapture(path)
        self.skip = skip
        self.op = op
        try:
            os.mkdir(self.op)
        except FileExistsError:
            pass

    def extract(self,*output):
        i=0
        count=0

        for k in output:
            try:
                os.mkdir(f'{self.op}/{k}')
            except FileExistsError:
                pass

        while True:
            _, img = self.cap.read()
            try:
                img = cv2.resize(img, None, fx=0.4, fy=0.4)
            except:
                break

            dt = datetime.now()
            cv2.imwrite(f'{self.op}/{output[i]}/{dt.year}-{dt.month}-{dt.day}|{dt.hour}:{dt.minute}:{dt.second}::{dt.microsecond}.jpg',img)
            count+=self.skip
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, count)

            i+=1
            i=i%len(output)

class LiveDetect(ObjectDetector):
    def write_from_video(self,path,write_dir="Result"):
        cap = cv2.VideoCapture(path)
        
        while True:
            frame,image = cap.read()
            try:
                img_arr = self.detect_object(image,detected_only=True)
                dt = datetime.now()
                img_nm = f'{dt.year}-{dt.month}-{dt.day}|{dt.hour}:{dt.minute}:{dt.second}::{dt.microsecond}.jpg'
                try:
                    if img_arr.all() != None:
                        cv2.imwrite(f"{write_dir}/{img_nm}", img_arr)
                except AttributeError:
                    pass
            except:
                pass

    def show_from_video(self,path):
        cap = cv2.VideoCapture(path)
        
        while True:
            frame,image = cap.read()
            try:
                img_arr = self.detect_object(image)
                cv2.imshow("img",img_arr)
                key = cv2.waitKey(1)
                if key == 27 & 0xFF == ord('q') :
                    break
            except:
                pass
        cap.release()
        cv2.destroyAllWindows()
                    
    def write_from_dir(self,read_dir="Output",read="A",write_dir="Result"):
        try:
            path = os.path.join(write_dir,read)
            os.mkdir(path)
        except FileNotFoundError:
            os.mkdir(write_dir)
            os.mkdir(path)
        except FileExistsError:
            pass
        g=0
        while True:
            f=0
            imgs=os.path.join(read_dir,read)
            for i in os.listdir(imgs):
                f=1
                g=0
                selected_img = os.path.join(imgs,i)
                img_arr = self.detect_object(selected_img,detected_only=True)
                os.remove(selected_img)

                dt = datetime.now()
                img_nm = f'{dt.year}-{dt.month}-{dt.day}|{dt.hour}:{dt.minute}:{dt.second}::{dt.microsecond}.jpg'
                try:
                    if img_arr.all() != None:
                        cv2.imwrite(f"{path}/{img_nm}", img_arr)
                except AttributeError:
                    pass
            if f==0 and g==0:
                print("No Images in Dir")
                g=1
                
    def show_from_dir(self,read_dir="Output",read="A"):
        while True:
            f=0
            imgs=os.path.join(read_dir,read)
            for i in os.listdir(imgs):
                f=1
                g=0
                selected_img = os.path.join(imgs,i)
                img_arr = self.detect_object(selected_img)
                cv2.imshow("img",img_arr)
                key = cv2.waitKey(1)
                if key == 27 & 0xFF == ord('q') :
                    break

