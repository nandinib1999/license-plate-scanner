from flask import * 
import cv2
from read_text import read_text
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  
 
@app.route('/')  
def upload():  
    return render_template("upload.html")

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = read_text(img)
            print(text)
            #print('upload_image filename: ' + filename)
            # flash('Image successfully uploaded and displayed')
            return render_template('success.html', filename=filename, name=text)
        else:
            # flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)  
            # f.save(f.filename)    
  
if __name__ == '__main__':  
    app.run(debug=True)  