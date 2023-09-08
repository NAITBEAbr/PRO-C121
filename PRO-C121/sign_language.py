import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

finger_fold_status = []

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)

    lm_list = []

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

    if lm_list:  
        for tip in finger_tips:
            if tip < len(lm_list):  
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)
            
                
                if tip - 3 >= 0 and lm_list[tip].x < lm_list[tip - 3].x:
                    cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_status.append(True)  
                else:
                    finger_fold_status.append(False)  

        if all(finger_fold_status):
            if thumb_tip < len(lm_list):  
                
                if thumb_tip - 1 >= 0 and thumb_tip - 2 >= 0 and lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y:
                    print("CURTI")
                    cv2.putText(img, "CURTI", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    print("NÃO CURTI")
                    cv2.putText(img, "NÃO CURTI", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        for i, finger_tip in enumerate(finger_tips):
            if finger_tip < len(lm_list):  
                x, y = int(lm_list[finger_tip].x * w), int(lm_list[finger_tip].y * h)
                is_folded = finger_fold_status[i]

                if is_folded:
                    cv2.circle(img, (x, y), 15, (0, 255, 0), 2)  
                else:
                    cv2.circle(img, (x, y), 15, (0, 0, 255), 2)  

    cv2.imshow("Detector de Mãos", img)
    cv2.waitKey(1)
