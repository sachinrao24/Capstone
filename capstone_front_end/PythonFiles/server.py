
from flask import Flask
from flask_cors import CORS, cross_origin
import datetime
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
  
# Route for seeing a data
@app.route('/bicepcurl')
def bicepcurl():
    import mediapipe as mp
    import numpy as np
    import cv2
    mp_drawing=mp.solutions.drawing_utils
    mp_pose=mp.solutions.pose

    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None
    wrongpostureupmessage='Incorrect'
    correctpostureupmessage='correct'
    wrongposture=True
    correctposture=False

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                ear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
                hips = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                
                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
                angle2=calculate_angle(ear,hips,knee)
                # Visualize angle
                cv2.putText(image, str(angle), 
                            tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                cv2.putText(image, str(angle2), 
                            tuple(np.multiply(hips, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                # Curl counter logic
                if angle > 165 and angle2>170:
                    stage = "down"
                    wrongposture=False
                    correctposture=True
                if angle2<170:
                    wrongposture=True
                    correctposture=False
                if angle < 30 and angle2>170 and stage =='down':
                    wrongposture=False
                    correctposture=True
                    stage="up"
                    counter +=1
                    print(counter)
                        
            except:
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
            
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            if wrongposture:
                cv2.putText(image,str(wrongpostureupmessage),
                            (10,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
            if correctposture:
                cv2.putText(image,str(correctpostureupmessage),
                            (10,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2,cv2.LINE_AA)
            
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
    return "Done"
      
@app.route('/legextensions')
def legextensions():
    # CODE FOR LEG EXTENSIONS HERE

@app.route('/lunges')
def legextensions():
    # CODE FOR LEG EXTENSIONS HERE

@app.route('/pushup')
def legextensions():
    # CODE FOR LEG EXTENSIONS HERE

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=5000)