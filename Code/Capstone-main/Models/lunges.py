import mediapipe as mp
import numpy as np
import cv2
from mediapipe.framework.formats import landmark_pb2
import joblib

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
lunges_coordinates = {(11, 23),
                      (12, 24),
                      (23, 25),
                      (23, 24),
                      (25, 27),
                      (24, 26),
                      (26, 28)}
lunges_connections = frozenset(lunges_coordinates)

cap = cv2.VideoCapture(0)

# Lunge counter variables
counter = 0 
stage = None
form = None

# function to convert angles to a value easy to use for lunge logic
def validate_angle(ang) :
    n = (ang-170)*0.05
    return (n >= 0 and n <= 1)

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
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee =  [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee =  [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            
            # Calculate angle
            right_knee_angle = calculate_angle(right_hip,right_knee,right_ankle)
            left_knee_angle = calculate_angle(left_hip,left_knee,left_ankle)
            body_straight = calculate_angle(left_shoulder,left_hip,left_knee)
            
            # Visualize angle
            cv2.putText(image, str(round(right_knee_angle, 2)), 
                           tuple(np.multiply(right_knee, webcam_dimensions).astype(int)), 
                           font, 0.5, white, 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(round(left_knee_angle, 2)), 
                           tuple(np.multiply(left_knee, webcam_dimensions).astype(int)), 
                           font, 0.5, white, 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(body_straight), 
                           tuple(np.multiply(left_hip, webcam_dimensions).astype(int)), 
                           font, 0.5, white, 2, cv2.LINE_AA
                                )
            # Lunge counter logic
            if (left_knee_angle > 90 and right_knee_angle < 90) or (right_knee_angle > 90 and left_knee_angle < 90):
                stage = "front"
                form = "correct"
            else : 
                form = "incorrect"
                
            if validate_angle(body_straight) :
                form = "correct"
                
            if not validate_angle(left_knee_angle) and validate_angle(right_knee_angle) and stage == 'front' :
                form = "incorrect"
                
            if validate_angle(left_knee_angle) and validate_angle(right_knee_angle) and stage == 'front' :
                stage="back"
                form = "correct"
                counter +=1
                    
        except:
            pass

         # Render detections
        if form == "incorrect":
            mp_drawing.draw_landmarks(image, results.pose_landmarks, lunges_connections,
                                    mp_drawing.DrawingSpec(color=grey, thickness=0, circle_radius=0), 
                                    mp_drawing.DrawingSpec(color=red, thickness=2, circle_radius=2))
            
        elif form == "correct":
            mp_drawing.draw_landmarks(image, results.pose_landmarks, lunges_connections,
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

joblib.dump(lunges, 'classifier.joblib')