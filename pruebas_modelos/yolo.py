import cv2
import numpy as np
import time
import colorsys
import argparse

path = "redes/"
path_archivos_test = "archivos_test/"

def YoloDetect(img_path,img_out,weights_file,cfg_file):

    img = cv2.imread(img_path)
    #color de las cajas
    _HSV = [(1.0 * x / 256, 1.0, 1.0) for x in range(256)]
    _COLORS = list(map(lambda x: colorsys.hsv_to_rgb(*x), _HSV))
    _COLORS = list(
        map(
            lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
            _COLORS,
        )
    )
    BBOX_COLORS = []
    _OFFSET = [0, 8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    for i in range(256):
        BBOX_COLORS.append(_COLORS[(i * 16) % 256 + _OFFSET[(i * 16) // 256]])


    #clases de yolo
    classes = []
    with open(path + 'coco.names', 'r') as f:
        classes = f.read().splitlines()

    height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(
        img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net = cv2.dnn_DetectionModel(cfg_file, weights_file)
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
            cv2.rectangle(img, top_left, bottom_right, bbox_color, 2)
            # Draw text box
            bbox_text = "{}: {:.1%}".format(
                classes[class_id], round(confidences[i], 2))
            t_size = cv2.getTextSize(bbox_text, 0, fontScale=0.4, thickness=1)[0]
            cv2.rectangle(
                img,
                top_left,
                (top_left[0] + t_size[0], top_left[1] - t_size[1] - 3),
                bbox_color,
                -1,
            )
            # Draw text
            cv2.putText(
                img,
                bbox_text,
                (top_left[0], top_left[1] - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.4,
                color=(255 - bbox_color[0], 255 -
                    bbox_color[1], 255 - bbox_color[2]),
                thickness=1,
                lineType=cv2.LINE_AA,
            )
    except Exception as e:
        print(e)

    cv2.imwrite(img_out,img)
    print("Imagen guardada: {}".format(img_out))



if __name__ == "__main__":
    t1 = time.time()
    # se crea un lector de argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cfg", type=str, default=path + "yolov3.cfg",
                    help="Ingrese el archivo de configuracion")
    ap.add_argument("-y", "--weights", type=str, default=path + "yolov3.weights",
                    help="ingrese los pesos del yolo")
    ap.add_argument("-i", "--img", type=str, default=path_archivos_test + "imagen_prueba.jpg",
                    help="ingrese la imagen a procesar")
    ap.add_argument("-o", "--salida", type=str, default=path_archivos_test + "salida_yolo.jpg",
                    help="ingrese la imagen de salida")
    
    # se pasan a variables los argumentos
    args = vars(ap.parse_args())

    YoloDetect(args["img"],args["salida"],args["weights"],args["cfg"])
    
    print("Tiempo de procesamiento: {:.2f}s".format(time.time()-t1))
    


