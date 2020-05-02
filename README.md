# License Plate Scanner
Using custom YoloV3 and PyTesseract, license plate has been detected and text has been extracted

To detect the license plate from the car image, I have trained a custom YoloV3 object detection program. The object detector was trained on the dataset obtained from https://www.kaggle.com/dataturks/vehicle-number-plate-detection and scraped some images from Google. Each image was manually annotated using LabelImg.

After detecting the license plate, the license plate image is passed through an image processing pipeline which includes techniques like Gaussian Blur, Binary Thresholding, Deskews, etc to remove the noise. The processed image is then passed to PyTesseract to extact the text from it.

The model weights of trained YoloV3 can be downloaded from https://drive.google.com/uc?export=download&id=1YXEKbYNLzfYpMcIkZ3h3UbeqfJ8vn7H3. Custom YoloV3 model was trained on Google Colab for about 3-4 hours. The .ipynb file for training the object detection model is **Train_YoloV3_.inpyb**. It makes use of Darknet.

Using Flask framework, I have created a web app where an image file can be uploaded and it returns the detected text.

## Libraries Used
1. OpenCV
2. PyTesseract
3. Flask
4. Deskew

## Usage
The following command can be used to run the web app.
```python app.py```
Go to ```http://127.0.0.1:5000/```
