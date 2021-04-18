import cv2
import os
from django.conf import settings
# from mtcnn import MTCNN
classifier = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR, 'haarcascade_frontalface_default.xml'))


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        ######################### MTCNN CODE ##########################

        # if ret:
        # 	detector = MTCNN()
        # 	try:
        # 		faces = detector.detect_faces(frame)
        # 		box=faces[0]['box']
        # 		cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0,0,255), 1)
        # 	except:
        # 		pass
        # 	frame_flip = cv2.flip(frame,1)
        # 	ret, jpeg = cv2.imencode('.jpg', frame_flip)
        # 	return jpeg.tobytes()

        ####################### CASCADE CLASSIFIER #####################

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bboxes = classifier.detectMultiScale(gray)
            for box in bboxes:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 1)
                FaceFileName = ".\captured_images\img.jpg"
                status = cv2.imwrite(FaceFileName, frame)
                crop_img = frame[y:y2, x:x2]
                FaceFileName = ".\captured_images\img2.jpg"
                status = cv2.imwrite(FaceFileName, crop_img)
                print(status)
            frame_flip = cv2.flip(frame, 1)
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
            return jpeg.tobytes()
