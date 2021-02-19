from mtcnn import MTCNN
import cv2

# # Code for Video

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    detector = MTCNN()
    try:
        faces = detector.detect_faces(frame)
        box=faces[0]['box']
        cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0,0,255), 1)
    except:
        pass
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()



# # Code for Image

image = cv2.imread('image.jpg')
detector = MTCNN()
try:
    faces = detector.detect_faces(image)
    box=faces[0]['box']
    cv2.rectangle( image, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0,0,255), 1)
    img = image[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]

except:
    pass
while True:
    cv2.imshow('Image',img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
