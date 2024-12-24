import cv2
import mediapipe as mp
import numpy as np
import time

# Inisialisasi Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

def calculate_similarity(img_left, img_right):
    height, width = img_left.shape[:2]
    left_gray = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    right_resized = cv2.resize(right_gray, (width, height))
    diff = cv2.absdiff(left_gray, right_resized)
    score = 100 - np.mean(diff) * 100 / 255
    return max(0, min(100, round(score)))

def draw_instruction_box(frame, text, countdown):
    h, w, _ = frame.shape
    box_width, box_height = 610, 150
    top_left_x = (w - box_width) // 2
    top_left_y = max(0, int(h * 0.2))
    bottom_right_x = top_left_x + box_width
    bottom_right_y = top_left_y + box_height
    overlay = frame.copy()
    cv2.rectangle(overlay, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 128, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)
    if len(text) > 50:
        split_index = text[:50].rfind(" ")
        text1 = text[:split_index]
        text2 = text[split_index+1:]
        cv2.putText(frame, text1, (top_left_x + 20, top_left_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, text2, (top_left_x + 20, top_left_y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    else:
        cv2.putText(frame, text, (top_left_x + 20, top_left_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, str(countdown), (top_left_x + box_width // 2 - 20, top_left_y + 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

image_paths = ["F:\\Tubes Mulmed\\data\\1.png", "F:\\Tubes Mulmed\\data\\2.png"]
current_image_index = 0
cap = cv2.VideoCapture(0)
session, countdown, countdown_start_time = 1, 5, None
stop_time, is_nodding, accuracy_displayed = None, False, False
nilaiAkurasi, frame_count, sesi2_start_time = None, 0, None
process_frame_interval, process_frame_counter = 5, 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    process_frame_counter += 1

    if process_frame_counter % process_frame_interval == 0:
        results = face_mesh.process(rgb_frame)
    if session == 1:
        if countdown_start_time is None:
            countdown_start_time = time.time()
        elapsed_time = time.time() - countdown_start_time
        if elapsed_time >= 1:
            countdown -= 1
            countdown_start_time = time.time()
        draw_instruction_box(frame, "Anggukan Kepalamu Untuk Mengetes Seberapa Cepat Kamu", countdown)
        if countdown <= 0:
            session, sesi2_start_time = 2, time.time()

    elif session == 2 and current_image_index < len(image_paths):
        image = cv2.imread(image_paths[current_image_index])
        if image is None:
            print(f"Gambar {image_paths[current_image_index]} tidak ditemukan.")
            current_image_index += 1
            continue
        scale_factor = 0.4
        img_height = int(height * scale_factor)
        img_width = int(image.shape[1] * img_height / image.shape[0])
        image = cv2.resize(image, (img_width, img_height))
        mid_x = image.shape[1] // 2
        img_left, img_right = image[:, :mid_x], image[:, mid_x:]

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                forehead_x = int(face_landmarks.landmark[10].x * width)
                forehead_y = int(face_landmarks.landmark[10].y * height) - int(img_height * 1.2)
                left_start_x = max(0, forehead_x - mid_x)
                right_start_x = forehead_x
                if left_start_x + mid_x <= width:
                    frame[forehead_y:forehead_y+img_height, left_start_x:left_start_x+mid_x] = img_left
                if right_start_x + mid_x <= width:
                    rotation_matrix = cv2.getRotationMatrix2D((mid_x // 2, img_height // 2), frame_count % 360, 1.0)
                    rotated_img_right = cv2.warpAffine(img_right, rotation_matrix, (mid_x, img_height))
                    frame[forehead_y:forehead_y+img_height, right_start_x:right_start_x+mid_x] = rotated_img_right
                top_y = int(face_landmarks.landmark[10].y * height)
                chin_y = int(face_landmarks.landmark[152].y * height)
                if chin_y - top_y > int(0.05 * height):
                    is_nodding, stop_time = True, time.time()
                    nilaiAkurasi = int(calculate_similarity(img_left, rotated_img_right))
        frame_count += 1
        if is_nodding and stop_time and time.time() - stop_time >= 5:
            session = 3

    elif session == 3 and nilaiAkurasi is not None:
        accuracy_text = f"Nilai keakuratan kamu sebesar {nilaiAkurasi}%"
        text_size = cv2.getTextSize(accuracy_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x, text_y = (width - text_size[0]) // 2, height // 2
        cv2.putText(frame, accuracy_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Reaction Time", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
