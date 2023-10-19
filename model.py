from ultralytics import YOLO
import cv2
import torch
import os
from datetime import datetime

def detect_live_camera(cam_num):
    # start webcam
    cap = cv2.VideoCapture(f"/dev/video{cam_num*2}")
    cap.set(3, 640)
    cap.set(4, 480)

    # model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    person_net = YOLO("./models/yolov8n.pt")
    smoking_net = YOLO("./models/cigarette_detection.pt")

    max_iters = 3
    iters_since_detection = max_iters+1
    clip_frames = []
    clip_saved = True

    if not os.path.exists(f'./live/cam{cam_num}'):
        os.makedirs(f'./live/cam{cam_num}')

    while True:
        success, img = cap.read()

        results = person_net(img, classes=0, stream=True, vid_stride=1, iou=0.2, device = device, verbose=False)

        s_boxes = []

        # Iterate through the results
        for i, r in enumerate(results):
            # Get the bounding boxes and class labels
            person_boxes = r.boxes.xyxy 
            classes = r.boxes.cls 

            # Iterate through the bounding boxes and class labels
            for j, (person_box, cls) in enumerate(zip(person_boxes, classes)):
                # Convert the person bounding box coordinates to integers
                x_min_p, y_min_p, x_max_p, y_max_p = map(int, person_box)
                # Crop the image to the dimensions of the bounding box
                cropped_image = r.orig_img[y_min_p:y_max_p, x_min_p:x_max_p]

                # Detect cigarettes within the cropped image
                s_results = smoking_net(cropped_image, iou=0, line_width=1, show_labels=False, max_det=1, device = device, verbose = False)

                for s_r in s_results:
                    
                    if len(s_r.boxes) > 0:
                        
                        if iters_since_detection > max_iters:
                            clip_name = datetime.today().strftime('%d-%m-%Y--%H-%M-%S')
                            folder_name = f'/cam{cam_num}' #+ datetime.today().strftime('%d-%m-%Y')

                        iters_since_detection = 0
                        clip_saved = False

                        s_box = s_r.boxes.xyxy[0].tolist() 

                        # Scale the coordinates back to the original image space
                        x_min_s, y_min_s, x_max_s, y_max_s = s_box
                        x_min_s += x_min_p
                        x_max_s += x_min_p
                        y_min_s += y_min_p
                        y_max_s += y_min_p

                        x_min_s, y_min_s, x_max_s, y_max_s = int(x_min_s), int(y_min_s), int(x_max_s), int(y_max_s)

                        s_boxes.append([x_min_s, x_max_s, y_min_s, y_max_s])
                    
                    else:
                        iters_since_detection += 1

        # Save the original image with the scaled cigarette bounding box
        original_image_with_cigarette_box = r.orig_img.copy()

        for box in s_boxes:
            cv2.rectangle(original_image_with_cigarette_box, (box[0], box[2]), (box[1], box[3]), (0, 255, 0), 2)

        # write live photo
        cv2.imwrite(f'live/cam{cam_num}/live_frame.jpg', original_image_with_cigarette_box)

        if iters_since_detection <= max_iters:
            clip_frames.append(original_image_with_cigarette_box)

        if not clip_saved and iters_since_detection > max_iters: 

            if not os.path.exists(f'./clips/{folder_name}'):
                os.makedirs(f'./clips/{folder_name}')

            height, width, _ = original_image_with_cigarette_box.shape
            out_name = f'./clips/{folder_name}/{clip_name}.mp4' 
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
            frame_rate = 1 
            frame_size = (width, height) 
            out = cv2.VideoWriter(out_name, fourcc, frame_rate, frame_size)

            for frame in clip_frames:  
                out.write(frame)

            out.release()

            clip_frames = []
            clip_saved = True
        #cv2.imshow('Webcam', original_image_with_cigarette_box)
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()   
