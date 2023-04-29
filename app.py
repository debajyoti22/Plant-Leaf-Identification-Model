import tensorflow
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np

from tensorflow.keras.models import load_model

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename


def recognise(value):

  loaded_model=load_model('D:\Leaf Model\content\inception_stage2.hdf5')
  #taking value
  img_path = value
  img = image.load_img(img_path, target_size=(256, 256))
  x = image.img_to_array(img)
  x = preprocess_input(x)
  img = image.load_img(img_path, target_size=(256, 256))
  x = image.img_to_array(img)
  x = preprocess_input(x)

  x = np.expand_dims(x, axis=0)
  preds = loaded_model.predict(x)
  # print(preds)

  alpha=" "
  labels=[]
  desc=""
  for i in range(0, 11): 
      if i==0:
        alpha="Black_grass"
        labels.append(alpha)
      if i==1:
        alpha="Charlock"
        labels.append(alpha)
      if i==2:
        alpha="Cleavers"
        labels.append(alpha)
      if i==3:
        alpha="Common Chickweed"
        labels.append(alpha)
      if i==4:
        alpha="Common wheat"
        labels.append(alpha)
      if i==5:
        alpha="Fat Hen"
        labels.append(alpha)
      if i==6:
        alpha="Loose Silky-bent"
        labels.append(alpha)
      if i==7:
        alpha="Maize"
        labels.append(alpha)
        desc="Maize, also known as corn, is a cereal crop that is widely grown around the world. It is a tall annual plant that can grow up to 3-4 meters high and produces large ears of kernels. Maize is a staple food for many cultures and is used for animal feed, biofuels, and various industrial applications. It is a rich source of carbohydrates, fiber, and essential nutrients such as vitamin B and minerals. Maize farming has also contributed significantly to the global economy."
      if i==8:
        alpha="Scentless Mayweed"
        labels.append(alpha)
      if i==9:
        alpha="Shepherds Purse"
        labels.append(alpha)
      if i==10:
        alpha="Small-flowered Cranesbill"
        labels.append(alpha)
      if i==11:
        alpha="Sugar beet"
        labels.append(alpha)
#Search the max value in prediction

  # return(labels[np.argmax(preds)])
  print(labels[np.argmax(preds)])
  data = labels[np.argmax(preds)]
  print(100*preds.max())  
  data2 = 100*preds.max() 
  return data,data2,desc


# app = Flask(__name__)
# @app.route("/",methods=["GET","POST"])
# def Index():
#     if req.method == "POST":
#         url = req.form.get("url")        
#         url_content = recognise(url) 
#         return render_template("main1.html",value2=url_content)
        
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)

#*********************************************************

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        flash('Image successfully uploaded')
        value = 'static/uploads/'+filename     
        
        answer1,answer2,desc = recognise(value)
        return render_template("main1.html",value2=answer1,value3=answer2,desc=desc,filename=value)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

#------------------------------------------------------------------------------
 
# @app.route('/display/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     value = 'static/uploads/'+filename
    
#     return redirect(url_for(filename=value), code=301)
    
    

 
if __name__ == "__main__":
    app.run()