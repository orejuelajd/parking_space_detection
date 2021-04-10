import numpy as np
import argparse
import time
import cv2

path = "redes/"
path_archivos_test = "archivos_test/"

def caffeDetect(img_path,salida):
    # initialize the list of class labels MobileNet SSD was trained to
    # detect
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]

    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe(path + "MobileNetSSD_deploy.prototxt", path + "MobileNetSSD_deploy.caffemodel")


    frame = cv2.imread(img_path)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    (H, W) = frame.shape[:2]


    # convert the frame to a blob and pass the blob through the
    # network and obtain the detections
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
    net.setInput(blob)
    detections = net.forward()
    rects= []
    confidences = []
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            idx = int(detections[0, 0, i, 1])

            # if the class label is not a person, ignore it
            if CLASSES[idx] != "car":
                continue

            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")

            rects.append([int(startX), int(startY), int(endX), int(endY)])
            confidences.append(confidence)
    contador = 0
    try:
        for rec in rects:
            x,y,w,h = rec
            label = "car " + str(confidences[contador])
            contador = contador + 1
            cv2.rectangle(frame, (x,y),(w,h),(0,255,0), 2)
            cv2.putText(frame, str(label), (x,y-5),cv2.FONT_HERSHEY_PLAIN,1, (0,255, 0), 2)
    except Exception as e:
        print(e)
    cv2.imwrite(salida, frame)

if __name__ == "__main__":
    t1 = time.time()
    # se crea un lector de argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--img", type=str, default=path_archivos_test + "imagen_prueba.jpg",
                    help="ingrese la imagen a procesar")
    ap.add_argument("-o", "--salida", type=str, default=path_archivos_test + "salida_caffe.jpg",
                    help="ingrese la imagen de salida")
    
    # se pasan a variables los argumentos
    args = vars(ap.parse_args())

    caffeDetect(args["img"],args["salida"])
    
    print("Tiempo de procesamiento: {:.2f}s".format(time.time()-t1))