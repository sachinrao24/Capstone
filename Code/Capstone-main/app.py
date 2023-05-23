from flask import Flask, render_template, request, url_for, redirect
import joblib
import cv2

app = Flask(__name__)

# client = MongoClient('  ', 27017, username = " ", password = " ")  # first argument is the localhost name , second is mongodb localhost port number

# db = client.flask_db  # flask_db is database name

bicep_curls = joblib.load('BicepCurls.joblib')
# lunges = joblib.load('Lunges.joblib')
# pushups = joblib.load('Pushups.joblib')
# leg_extensions = joblib.load('LegExtensions.joblib')


@app.route("/")
def index() :
    
    """
        Index page navigation
    """
    
    return render_template('capstone_front_end\public\index.html')

@app.route("/exercises")
def exercises():

    """
        4 Different exercises page 
    """

    return render_template('capstone_front_end\public\index.html')

@app.route("/MediaPipeOutput")
def cam_instance():

    """
        Mediapipe camera instance 
    """

    return render_template('capstone_front_end\public\index.html')


if __name__ =='__main__':
    app.run(debug=True)

# import cv2
# import numpy as np
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import base64

# app = Flask(__name__)
# CORS(app)

# @app.route('/check_form', methods=['POST'])
# def check_form():
#     data = request.json
#     image_data = data['imageData']
#     # convert base64-encoded image to OpenCV format
#     image_bytes = bytes(image_data, encoding='utf-8')
#     image = cv2.imdecode(np.frombuffer(base64.b64decode(image_bytes), dtype=np.uint8), -1)
    
#     # run your Python code on the image here
    
#     return jsonify({'message': 'success'})

# if __name__ == '__main__':
#     app.run(debug=True)