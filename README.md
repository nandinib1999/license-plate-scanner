# license-plate-scanner
Using custom YoloV3 and PyTesseract, license plate has been detected and text has been extracted

To detect the license plate from the car image, I have trained a custom YoloV3 object detection program. The object detector was trained on the dataset obtained from https://www.kaggle.com/dataturks/vehicle-number-plate-detection and some images from Google.

After detecting the license plate, the license plate image is passed through an image processing pipeline which includes techniques like Gaussian Blur, Binary Thresholding to remove the noise. The processed image is then passed to PyTesseract to extact the text from it.
