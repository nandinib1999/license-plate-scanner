import cv2
import numpy as np 

###### Global Variables ######

net = cv2.dnn.readNet("yolov3_training.weights", "yolov3_training.cfg")
classes = ['license']
layers_names = net.getLayerNames()
outputLayers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

def detect_license_plate(img_small):
	if len(img_small.shape) == 3:
		height, width, channels = img_small.shape
	else:
		height, width = img_small.shape


	blob = cv2.dnn.blobFromImage(img_small, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

	net.setInput(blob)
	out = net.forward(outputLayers)

	boxes = []
	confs = []
	class_ids = []
	for o in out:
		for detect in o:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.5:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
				

	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	font = cv2.FONT_HERSHEY_PLAIN
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			license_plate = img_small[y+2:y+h+2, x+2:x+w+2]
	return license_plate

if __name__ == '__main__':
	detect_license_plate()