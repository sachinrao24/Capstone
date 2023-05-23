import mediapipe as mp
import numpy as np
import cv2
from mediapipe.framework.formats import landmark_pb2
from sklearn.externals import joblib

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles
PoseLandmark = mp.solutions.pose.PoseLandmark

####### FIXED VARIABLES ##########
font = cv2.FONT_HERSHEY_TRIPLEX
webcam_dimensions = [640, 480]

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (97,250,2)
red = (19,3,252)
grey = (131, 133, 131)
light_blue = (237, 215, 168)

####### FUNCTIONS ##########
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle 

def render_status_box(counter, stage, fontScale, form):
    cv2.rectangle(image, (0,0), (235,75), light_blue, -1)
    cv2.rectangle(image, (300, 0), (640, 75), white, -1)
    cv2.putText(image, 'REPS', (15,12), font, 0.5, black, 1, cv2.LINE_AA)
    cv2.putText(image, str(counter), (10,60), font, fontScale, white, 2, cv2.LINE_AA)
    cv2.putText(image, 'STAGE', (105,12), font, 0.5, black, 1, cv2.LINE_AA)
    cv2.putText(image, stage, (60,60), font, 2, white, 2, cv2.LINE_AA)
    
    if form == "correct":
        cv2.putText(image, form, 
                (330, 50), 
                font, 2, green, 2, cv2.LINE_AA)
    else:
        cv2.putText(image, form, 
                (315, 50), 
                font, 2, red, 2, cv2.LINE_AA)


######### START CHECKING EXERCISE ###########
pushup_coordinates = {(11, 23),
                       (12, 24),
                       (23, 25),
                       (24, 26)}
pushup_connections = frozenset(pushup_coordinates)

cap = cv2.VideoCapture(0)

# Push-up counter variables
counter = 0 
stage = None
form = None

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    cv2.namedWindow('Mediapipe Feed', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Mediapipe Feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
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
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            # Calculate angles
            left_hip_angle = calculate_angle(left_shoulder, left_hip, left_ankle)
            left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            right_hip_angle = calculate_angle(right_shoulder, right_hip, right_ankle)
            right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Visualize angle
            cv2.putText(image, str(round(left_hip_angle, 2)), 
                           tuple(np.multiply(left_hip, webcam_dimensions).astype(int)), 
                           cv2.FONT_HERSHEY_TRIPLEX, 0.5, white, 2, cv2.LINE_AA)
            
            cv2.putText(image, str(round(right_hip_angle, 2)), 
                           tuple(np.multiply(left_hip, webcam_dimensions).astype(int)), 
                           cv2.FONT_HERSHEY_TRIPLEX, 0.5, white, 2, cv2.LINE_AA)
        except:
            pass

        
        # Form data and pushup counter logic
        if left_hip_angle < 155 or right_hip_angle < 155:
            form = "incorrect"
        elif left_hip_angle > 155 or right_hip_angle > 155:
            form = "correct"
        if left_elbow_angle < 70 or right_elbow_angle < 70:
            stage="down"
        elif (left_elbow_angle > 160 or right_elbow_angle > 160) and stage=="down":
            stage="up"
            counter+=1
            
        
         # Render detections
        if form == "incorrect":
            mp_drawing.draw_landmarks(image, results.pose_landmarks, pushup_connections,
                                    mp_drawing.DrawingSpec(color=grey, thickness=0, circle_radius=0), 
                                    mp_drawing.DrawingSpec(color=red, thickness=2, circle_radius=2))
            
        elif form == "correct":
            mp_drawing.draw_landmarks(image, results.pose_landmarks, pushup_connections,
                                    mp_drawing.DrawingSpec(color=grey, thickness=0, circle_radius=0), 
                                    mp_drawing.DrawingSpec(color=green, thickness=2, circle_radius=2))
            
    
        if counter < 10:
            render_status_box(counter, stage, 2, form)
        else:
            render_status_box(counter, stage, 1, form)
            
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

joblib.dump(pushups, 'classifier.joblib')