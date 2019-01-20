import cv2

count = 0
cap = cv2.VideoCapture('data/video.avi')
ret, image = cap.read()

print('Starting getting frames from video...')
while ret:
    cap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
    ret, image = cap.read()
    if not ret:
        break

    cv2.imwrite( 'data/videoframe/' + "frame%d.jpg" % count, image)
    count = count + 1

