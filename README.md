# Detección de Zonas de Parqueo Disponibles

**Integrantes:** 
[Heberth Martinez](https://github.com/hfmartinez)
[Francisco Pedroza ](https://github.com/franciscopedroza030595)
[Johan Loaiza](https://www.google.com)
[Juan David Orejuela](https://github.com/orejuelajd)

**Planteamiento del problema**

La congestión del tráfico causada por el vehículo es un problema alarmante a escala global el cual ha estado creciendo de manera exponencial. El problema de la disponibilidad de estacionamientos de automóviles es un contribuyente importante debido a que el parque automotor se incrementa con el paso de los años, adicionalmente, el tamaño de los vehículos en el segmento de lujo ha aumentado sus medidas. Por lo cual, buscar una plaza de aparcamiento es una actividad de rutina para muchas personas en ciudades de todo el mundo. Esta búsqueda quema alrededor de un millón de barriles de petróleo del mundo

todos los días.

A medida que la población mundial continúa urbanizando, sin un retiro del automóvil bien planificado y orientado a la conveniencia, estos problemas empeorarán [1]. Los estacionamientos simplemente han ignorado la problemática ya que no se han implementado tecnologías que permitan mejorar la eficiencia de estos, a partir de ello se genera la pérdida de tiempo en los conductores cuando buscan un lugar libre. También se generan situaciones peligrosas ya que mientras el conductor se enfoca en la búsqueda de un lugar libre se distrae de lo que pasa a su alrededor lo que aumenta la probabilidad de que cause un accidente.

Un sistema de estacionamiento inteligente mediante visión computacional podría obtener información sobre los espacio de estacionamiento disponibles en un área determinada realizando el proceso en tiempo real para ubicar los vehículos en los lugares disponibles y evitar la circulación innecesaria de las personas.

**Métodos**

Mediante el uso de tecnologías de visión computacional haciendo uso de modelos ya existentes para la detección y clasificación de objetos se seleccionan tres para realizar implementación y pruebas sobre el video seleccionado de un estacionamiento, en este se definen un número de ROIS(regiones de interés) las cuales se sabe pueden tienen una cantidad definida de automóviles dentro de las mismas e identificando y clasificando los automóviles en cada ROI se obtiene mediante una diferencia los espacio disponibles para la misma. Los ROIS son calculados haciendo uso de la librería Shapely para python que teniendo cuatro puntos o coordenadas genera un polígono de interés.Mediante el uso de la librería Tkinter para python se implementa una interfaz gráfica para visualizar las detecciones y la información del total de parqueaderos por ROI y la cantidad de

parqueaderos disponibles.

A continuación se enlista los 3 modelo implementado:

- Faster RCNN ( VGG16)
- YOLO
- Modelo con Tensor Flow(Faster RCNN ResNet 101)

Con la implementación de cada modelo se realiza el procesamiento frame a frame, donde se obtienen resultados para cada frame. El resultado esperado es obtener los cuadros delimitadores con su respectiva información de posición y mediante la lógica del software implementado definir si se encuentra dentro o no de una región de interés(ROI) y poder calcular la cantidad de parqueaderos disponibles dentro de la región de interés.

**Descripción los Modelos**

**Faster RCNN VGG 16**

Es una arquitectura de detección de objetos más famosa que emplea redes convolucionales, esta es compuesta por tres secciones las capas convolucionales, la red RPN (*Region Proposel Network*) y la capa de predicción de cuadros delimitadores y clases[5] los cuales componen la salida de la red.

1. Redes Convolucionales: Se encargan de aplicar filtros para extraer las características principales de las imágenes.
1. RPN: Se encarga de detectar las regiones de interés (*ROIs*) donde se encuentra el objeto y así predecir los cuadros delimitadores (*Bounding Boxes*) a estos objetos en la imagen.
1. Capa de Predicción: Emplea una capa densa en la red neuronal, con la cual se predice la clase de los objetos acotados en las regiones de interés.

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.001.png)

Imagen No. 1. Arquitectura de FasterRCNN

**YOLO:** Arquitectura popular para el reconocimiento de objetos con gran precisión disponible para ser implementada en tiempo real. ”only looks once” en el sentido de que se requiere que cada imagen o frame solo se propague una vez a través de la red neuronal para realizar predicciones[4]. La salida de YOLO entrega el reconocimiento de los diferentes objetos(clases) demarcados dentro de un cuadro delimitador(bounding box) y la información relacionada con la posición del centroide(x, y), el tamaño(alto, ancho) y el porcentaje de precisión de la clase asignada al objeto por la red.

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.002.png)

Imagen No. 2. Arquitectura de YOLO

**Modelo Faster RCNN ResNet 101:**

Resnet es el nombre reducido para Red Neuronal Residual

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.003.jpeg)

Imagen No. 3. Arquitectura de ResNet 101

**Datasets**

**Faster RCNN:**

- Entrenamiento mediante dataset de Open Image

**YOLO:**

- Entrenamiento mediante dataset de **COCO Dataset**:

Conjunto de datos de detección, segmentación y etiqueta de objetos a gran escala, este es patrocinado por Microsoft, Facebook, Mighty AI y CVDF.

Este dataset permite realizar  segmentación de objetos, reconocimiento en contexto por medio de un conjunto de datos de más de 330 mil imágenes, 1.5 millones de instancias de objeto y 80 categorías de objetos y 5 etiquetas por imagen. Para este caso solo se emplea la clase Carro para la detección de los objetos en la red YOLO.

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.004.jpeg)

Imagen 4. Imagen de ejemplo del dataset de MS-COCO

**Modelo Faster RCNN ResNet 101:**

- Entrenamiento mediante dataset privado(etiquetado manual) el cual consiste en en 930 Imágenes donde 600 pertenecen a imágenes y las 330 restantes pertenecen a personas y camiones.

**Resultados**

**Faster RCNN VGG 16:**

- Tiempo de ejecución extensos para procesamiento frame a frame.

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.005.jpeg)

Imagen 5. Resultado de Localización y Clasificación con FasterRCNN y VGG16

**YOLO:**

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.006.jpeg)

Imagen 6. Resultado de Localización y Clasificación con YOLO **Modelo Faster RCNN ResNet 101:**

![](https://raw.githubusercontent.com/orejuelajd/parking_space_detection/master/documentation/raw_files/Aspose.Words.10eed888-fc97-461d-b4bc-f1107494bcc1.007.jpeg)

Imagen 7. Resultado de Localización y Clasificación con FasterRCNN y ResNet 101



|Faster RCNN VGG 16 (CPU)|YOLO (CPU)|Modelo Faster RCNN ResNet 101 (GPU)|
| :- | - | :- |
|6.78 segundos|0.62 segundos|0.84 segundos|

Tabla 1. TIempos de procesamiento para un frame

***Nota**: La ejecución de los scripts se hizo en una computadora con las siguientes características: Intel Core i5-8400 CPU 2.8GHz, 16 Gb de RAM y GPU 1080 GTX de 4GB de VRAM.*

**Conclusiones**

- Debido a que la Faster RCNN VGG-16 debe propagar varias veces las imágenes por las diferentes configuraciones de la red el procesamiento de las imagen toma tiempos más altos.
- El ángulo de la cámara con la cual se capturan los videos a predecir es directamente proporcional a la precisión de la predicción, esta debe coincidir con las imágenes utilizadas en el proceso de entrenamiento.
- EL uso de python como lenguaje principal para realizar el procesamiento de imágenes y la implementación de arquitecturas de redes neuronales es muy cómodo gracias a la cantidad de librerías existentes.
- El sistema cumple la función para lo cual se desarrollo, pero se hace evidente la necesidad del uso de una máquina con GPU para realizar un procesamiento de imágenes en de forma óptima en ambientes productivos
- Aún cuando la red Faster RCNN con ResNet se entrenó con una menor cantidad de imágenes que las demás redes, se obtuvieron buenos resultados de detección y

localización debido al dataset usado para esta, ya que los datos de entrenamiento contienen imágenes de automóviles en una perspectiva similar a los que se encuentran en las tomas del video de prueba.

**Bibliografía**

1. Debaditya Acharya and Weilin Yan, “Real-time image-based parking occupancy detection using deep learning” Infrastructure Engineering, The University of Melbourne,[online]. Available:http://ceur-ws.org/Vol-2087/paper5.pdf
1. Ordonia Samuel, “Detecting cars in a parking lot using deep learning”, San Jose State University,[online].Available:https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1697& context=etd\_projects
1. Dwivedi Priya, “Find where to park in real time using OpenCV and Tensorflow”,towards data science,[online]. Available:https://towardsdatascience.com/find-where-to-park-in-real-time-using-opencv-and-t ensorflow-4307a4c3da03
1. ODSC - Open Data Science, “ Overview of the YOLO object Detection Algorithm”,[online]. Available: <https://medium.com/@ODSC/overview-of-the-yolo-object-detection-algorithm-7b52a745d3e0>
1. Achraf KHAZRI - “Faster RCNN Object detection”,[online]. Available: https://towardsdatascience.com/faster-rcnn-object-detection-f865e5ed7fc4#:~:text=Faster%2 0RCNN%20is%20an%20object,SSD%20(%20Single%20Shot%20Detector).
