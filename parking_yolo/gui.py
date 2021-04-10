# librerias necesarias
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import threading
import cv2
import time
import imutils
from PIL import Image
from PIL import ImageTk
import colorsys
#import pymongo
from shapely.geometry import Polygon, Point
import time
import datetime
import requests

class Application(tk.Frame):
    def getRegions(self):
        '''
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['test-database']
        collection = db['test-collection']
        data = collection.find_one({"key": "data"})
        '''
        json_data = {
            "ok": True,
            "Data": {
                "zonas":
                    [[[28, 250], [540, 215], [635, 270], [2, 305]],
                     [[28, 205], [470, 185], [635, 210], [2, 240]],
                     [[15, 330], [680, 300], [680, 385], [2, 390]]],
                "_id": "60661485beb3c8287ce37aea",
                "parqueadero": "60627ee130a8c321b4c17824",
                "totalZonas": 3,
                "totalPermitidos": 61,
                "__v": 0
            }
        }

        return json_data

    def createWidgets(self):
        self.pack(fill=tk.X)

        tab_parent = ttk.Notebook(self)

        s = ttk.Style()
        s.configure('estilo.TFrame', background='#000000')

        tab1 = ttk.Frame(tab_parent, style='estilo.TFrame')

        tab_parent.add(tab1, text="Visualización")

        # ========================================
        # ========= control de video =============
        # ========================================

        videoFrame = tk.LabelFrame(tab1, text="Video", borderwidth=0,
                                   font="helvetica 10 bold italic", fg="#FFFFFF", bg="#000000", padx=8, width=750)
        videoFrame.grid(row=0, column=0, sticky=tk.W +
                        tk.E+tk.S+tk.N, pady=5, padx=5)

        image = cv2.imread('data/parking.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = imutils.resize(image, width=700)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.videoPanel = tk.Label(videoFrame, image=image)
        self.videoPanel.image = image
        self.videoPanel.pack(side="left", pady=10)
        self.videoPanel.grid(row=0, column=0, sticky=tk.W)

        # ========================================
        # ======== control de espacios ===========
        # ========================================

        controlFrame = tk.LabelFrame(
            tab1, text="Control", font="helvetica 10 bold italic", fg="#FFFFFF", padx=8, width=250, bg="#000000", borderwidth=0)
        controlFrame.grid(row=0, column=1, sticky=tk.W +
                          tk.E+tk.S+tk.N, pady=5, padx=5)

        disponible = tk.Label(controlFrame, text="Libres",
                              font="helvetica 30 bold",  fg="#00ff00", bg="#000000")
        disponible.grid(row=0, column=0, sticky=tk.W, pady=4, padx=5)

        totalDisponible = tk.Label(controlFrame, textvariable=self.disponibles,
                                   font="helvetica 30 bold",  fg="#00ff00", bg="#000000")
        totalDisponible.grid(row=1, column=0, sticky=tk.W, pady=4, padx=5)

        ocupados = tk.Label(controlFrame, text="Ocupados",
                            font="helvetica 30 bold",  fg="#ff0000", bg="#000000")
        ocupados.grid(row=2, column=0, sticky=tk.W, pady=4, padx=5)

        #totalOcupados = tk.Label(controlFrame, textvariable=self.ocupados, 
        #                         font="helvetica 30 bold",  fg="#ff0000", bg="#000000")
        #totalOcupados.grid(row=3, column=0, sticky=tk.W, pady=4, padx=5)
        
        totalOcupadosZona0 = tk.Label(controlFrame, textvariable=self.ocupadosZona0, font="helvetica 30 bold",  fg="#ff0000", bg="#000000")
        totalOcupadosZona0.grid(row=3, column=0, sticky=tk.W, pady=4, padx=5)
        
        totalOcupadosZona1 = tk.Label(controlFrame, textvariable=self.ocupadosZona1, font="helvetica 30 bold",  fg="#ff0000", bg="#000000")
        totalOcupadosZona1.grid(row=4, column=0, sticky=tk.W, pady=4, padx=5)
        
        totalOcupadosZona2 = tk.Label(controlFrame, textvariable=self.ocupadosZona2, font="helvetica 30 bold",  fg="#ff0000", bg="#000000")
        totalOcupadosZona2.grid(row=5, column=0, sticky=tk.W, pady=4, padx=5)

        tab_parent.pack(expand=1, fill='both')

    def close(self):
        print("close")
        self.master.quit()

    def deteccionParking(self, coordenadas, p):
        poly = Polygon(coordenadas)
        point = Point(p)
        return poly.contains(point)

    def videoLoop(self):
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=30)
        while True:
            _HSV = [(1.0 * x / 256, 1.0, 1.0) for x in range(256)]
            _COLORS = list(map(lambda x: colorsys.hsv_to_rgb(*x), _HSV))
            _COLORS = list(
                map(
                    lambda x: (int(x[0] * 255),
                               int(x[1] * 255), int(x[2] * 255)),
                    _COLORS,
                )
            )
            BBOX_COLORS = []
            _OFFSET = [0, 8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
            for i in range(256):
                BBOX_COLORS.append(
                    _COLORS[(i * 16) % 256 + _OFFSET[(i * 16) // 256]])

            classes = []
            with open('data/coco.names', 'r') as f:
                classes = f.read().splitlines()
            vs = cv2.VideoCapture('data/procesado.mp4')
            
            net = cv2.dnn_DetectionModel(
                "data/yolov3.cfg", "data/yolov3.weights")

            json_data = self.getRegions()
            pts = np.array(json_data["Data"]["zonas"],np.int32)
            pts.reshape((-1,1,2))

            while True:
                total_presente = 0
                contadores = [0, 0, 0]
                ret, self.frame = vs.read()
                if not ret:
                    break
                self.frame = imutils.resize(self.frame, width=700)
                height, width, _ = self.frame.shape
                blob = cv2.dnn.blobFromImage(
                    self.frame, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

                net.setInput(blob)

                output_layers_names = net.getUnconnectedOutLayersNames()
                layerOutputs = net.forward(output_layers_names)

                boxes = []
                confidences = []
                class_ids = []

                for output in layerOutputs:
                    for detection in output:
                        scores = detection[5:]
                        class_id = np.argmax(scores)

                        confidence = scores[class_id]
                        if confidence > 0.3:
                            center_x = int(detection[0]*width)
                            center_y = int(detection[1]*height)
                            w = int(detection[2]*width)
                            h = int(detection[3]*height)

                            x = int(center_x-w/2)
                            y = int(center_y - h/2)

                            boxes.append([x, y, w, h, center_x, center_y])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.3)

                try:
                    for i in indexes.flatten():
                        x, y, w, h, cx, cy = boxes[i]
                        top_left = (x, y)
                        bottom_right = (x+w, y+h)
                        class_id = int(class_ids[i])
                        bbox_color = BBOX_COLORS[class_id]

                        # Draw box
                        cv2.rectangle(self.frame, top_left,
                                      bottom_right, bbox_color, 1)
                        # Draw text box
                        bbox_text = "{}: {:.1%}".format(
                            classes[class_id], round(confidences[i], 2))
                        t_size = cv2.getTextSize(
                            bbox_text, 0, fontScale=0.3, thickness=1)[0]
                        cv2.rectangle(
                            self.frame,
                            top_left,
                            (top_left[0] + t_size[0],
                             top_left[1] - t_size[1] - 3),
                            bbox_color,
                            -1,
                        )
                        # Draw text
                        cv2.putText(
                            self.frame,
                            bbox_text,
                            (top_left[0], top_left[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.3,
                            color=(255 - bbox_color[0], 255 -
                                   bbox_color[1], 255 - bbox_color[2]),
                            thickness=1,
                            lineType=cv2.LINE_AA,
                        )
                        salida = False
                        
                        if classes[class_id] == 'car' or 'truck':
                            total_zonas = json_data["Data"]["totalZonas"]
                            for i in range(total_zonas):
                                coordenadas = json_data["Data"]["zonas"][i]
                                salida = self.deteccionParking(
                                    coordenadas, (cx, cy))
                                if (salida):
                                    cv2.circle(self.frame, (cx, cy),
                                               3, (0, 255, 255), 2)
                                    total_presente = total_presente + 1
                                    contadores[i] = contadores[i] + 1
                                    #total_presente = total_presente + 1
                                    
                except Exception as e:
                    print(e)
                
                cv2.drawContours(self.frame, pts, -1, (0,0,255), 1)
                rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(rgb)
                image = ImageTk.PhotoImage(image)

                self.videoPanel.configure(image=image)
                self.videoPanel.image = image

                # self.ocupados.set(str(total_presente))
                self.disponibles.set(str(json_data["Data"]["totalPermitidos"] - total_presente))
                for index, contador in enumerate(contadores):
                    if(index == 0):
                        self.ocupadosZona0.set("Zona #0: " + str(contador))
                    elif(index == 1):
                        self.ocupadosZona1.set("Zona #1: " + str(contador))
                    elif(index == 2):
                        self.ocupadosZona2.set("Zona #2: " + str(contador))
                if datetime.datetime.now() >= endTime:
                    endTime = datetime.datetime.now() + datetime.timedelta(seconds=30)
                    data = {'totalPermitidos':contadores}
                    print(data)
                    response = requests.put('https://cv-mongoserver.herokuapp.com/api/rois/60706f423d7d85482c32fc88', data=data)
                    print(response.content)
                    print('------------------------------------------------------------------')
                    #for index, contador in enumerate(contadores):
                    #    print('contador ', [index], " :", contador)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        master.title("Parking")
        master.geometry("1100x450+0+0")
        master.resizable(False, False)
        master.configure(background='black')

        self.disponibles = tk.StringVar()
        # self.ocupados = tk.StringVar()
        self.ocupadosZona0 = tk.StringVar()
        self.ocupadosZona1 = tk.StringVar()
        self.ocupadosZona2 = tk.StringVar()
        self.disponibles.set("61")
        # self.ocupados.set("0")
        self.ocupadosZona0.set("Zona #0: 0")
        self.ocupadosZona1.set("Zona #1: 0")
        self.ocupadosZona2.set("Zona #2: 0")

        self.createWidgets()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

def main():
    root = tk.Tk()
    root.iconbitmap('.\data\icono.ico')
    app = Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    app.mainloop()
    
# metodo main
if __name__ == '__main__':
    main()