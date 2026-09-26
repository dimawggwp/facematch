import cv2
import numpy as np
import math
import mediapipe as mp

def calculate_angle(p1, p2):
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

def analyze_face(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None: 
        return 10

    # Используем базовый FaceMesh через инициализатор класса
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks: 
            return 10

        landmarks = results.multi_face_landmarks[0].landmark
        score = 50 

        left_tilt = calculate_angle((landmarks[133].x, landmarks[133].y), (landmarks[33].x, landmarks[33].y))
        right_tilt = calculate_angle((landmarks[362].x, landmarks[362].y), (landmarks[263].x, landmarks[263].y))
        
        if left_tilt < 0 and right_tilt > 0: score += 15
        else: score -= 5

        chin = landmarks[152].x
        left_jaw = landmarks[132].x
        right_jaw = landmarks[361].x
        symmetry_diff = abs(abs(chin - left_jaw) - abs(chin - right_jaw))
        score += max(0, 15 - (symmetry_diff * 100))

        score += np.random.randint(-5, 5) 
        return int(max(1, min(99, score)))