import cv2
import numpy as np
import torch

#################################### input section ####################################

video_source = "/home/lenovo/Desktop/Tasks_khloodmontaser/task2/AI Intern Video Tech Task.mp4"
video_capture = cv2.VideoCapture(video_source)
detection_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

#################################### logic section ####################################

# cashier_zone = np.array([(368, 139), (320, 0), (152, 0), (185, 186)], np.int32)

# Region of Interest (ROI)
roi_coordinates = [
    [136, 0], [15, 0], [15, 500], [1015, 500],
    [1015, 0], [326, 0], [311, 78], [306, 139],
    [188, 188]
]
region_of_interest = np.array(roi_coordinates, np.int32).reshape((-1, 1, 2))

# Function to draw the ROI on the frame
def draw_region_of_interest(frame):
    cv2.polylines(frame, [region_of_interest], isClosed=True, color=(255, 0, 0), thickness=2)
    return region_of_interest

# Function to check if a point is inside the region
def is_point_in_region(point, region):
    return cv2.pointPolygonTest(region, point, False) >= 0

while video_capture.isOpened():
    ret, frame = video_capture.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (1020, 500))
    
    aoi = draw_region_of_interest(frame)
    detection_results = detection_model(frame)

    count_people = 0
    for *bbox, confidence, class_id in detection_results.xyxy[0]:
        if int(class_id) == 0:  
            x_center = int((bbox[0] + bbox[2]) / 2)
            y_center = int((bbox[1] + bbox[3]) / 2)
            
            if is_point_in_region((x_center, y_center), aoi):
                count_people += 1
                
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)

#################################### output section ####################################

    # Display part
    text = f'No. of people: {count_people}'
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    
    cv2.rectangle(frame, (10, frame.shape[0] - 30), (10 + text_width, frame.shape[0] - 10 + baseline), (255, 255, 255), -1)
    cv2.putText(frame, text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow('People Counting in Designated Zone', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
