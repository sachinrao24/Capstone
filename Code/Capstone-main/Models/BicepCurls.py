import mediapipe as mp
import numpy as np
import cv2
from mediapipe.framework.formats import landmark_pb2
import joblib

class BicepCurls():
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

    def render_status_box(self, image, counter, stage, fontScale, form):
        cv2.rectangle(image, (0,0), (235,75), self.light_blue, -1)
        cv2.rectangle(image, (300, 0), (640, 75), self.white, -1)
        cv2.putText(image, 'REPS', (15,12), self.font, 0.5, self.black, 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10,60), self.font, fontScale, self.white, 2, cv2.LINE_AA)
        cv2.putText(image, 'STAGE', (105,12), self.font, 0.5, self.black, 1, cv2.LINE_AA)
        cv2.putText(image, stage, (60,60), self.font, 2, self.white, 2, cv2.LINE_AA)
        
        if form == "correct":
            cv2.putText(image, form, 
                    (330, 50), 
                    self.font, 2, self.green, 2, cv2.LINE_AA)
        else:
            cv2.putText(image, form, 
                    (315, 50), 
                    self.font, 2, self.red, 2, cv2.LINE_AA)

    ######### START CHECKING EXERCISE ###########
    def check_form(self):
        curl_coordinates = {(11, 12),
                            (11, 13),
                            (11, 23),
                            (12, 14),
                            (12, 24),
                            (13, 15),
                            (14, 16),
                            (23, 24),
                            (23, 25),
                            (24, 26)}
        curl_connections = frozenset(curl_coordinates)

        cap = cv2.VideoCapture(0)

        # Curl counter variables
        counter = 0 
        stage = None
        form = None

        ## Setup mediapipe instance
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
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
                    right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
                    right_ear = [landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].y]
                    right_hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    right_knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    
                    # Get coordinates
                    left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    
                    left_ear = [landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].y]
                    left_hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    left_knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    
                    # Calculate angle
                    left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                    right_arm_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                    
                    left_hip_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
                    right_hip_angle = self.calculate_angle(right_shoulder, right_hip, right_knee)
                    
                    # Visualize angle
                    cv2.putText(image, str(round(right_hip_angle, 2)), 
                                tuple(np.multiply(right_hip_angle, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(round(left_hip_angle, 2)), 
                                tuple(np.multiply(left_hip_angle, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    # Curl counter logic
                    if right_hip_angle < 170 or left_hip_angle < 170:
                        form = "incorrect"
                    else:
                        if right_arm_angle > 165 or left_arm_angle > 165:
                            stage = "down"
                            form = "correct"
                        elif (right_arm_angle < 30 or left_arm_angle < 30) and stage =='down':
                            form = "correct"
                            stage="up"
                            counter +=1
                            
                except:
                    pass
                    
                # Render detections
                if form == "incorrect":
                    self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.lunges_connections,
                                            self.mp_drawing.DrawingSpec(color=self.grey, thickness=0, circle_radius=0), 
                                            self.mp_drawing.DrawingSpec(color=self.red, thickness=2, circle_radius=2))
                    
                elif form == "correct":
                    self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.lunges_connections,
                                            self.mp_drawing.DrawingSpec(color=self.grey, thickness=0, circle_radius=0), 
                                            self.mp_drawing.DrawingSpec(color=self.green, thickness=2, circle_radius=2))
                    
            
                if counter < 10:
                    self.render_status_box(image, counter, stage, 2, form)
                else:
                    self.render_status_box(image, counter, stage, 1, form)  
                    
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                
                return image
            
            cap.release()
            cv2.destroyAllWindows()

joblib.dump(BicepCurls, 'BicepCurls.joblib')