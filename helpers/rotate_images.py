import cv2
import glob

import numpy as np

PATH_TO_IMAGES = '../data/images/train/kermit/kermit-train-images'


def rotate_image(image_path: str, direction: str):
    img = cv2.imread(image_path)

    h, w, c = img.shape
    h = h - 1
    w = w - 1

    empty_img = np.zeros([h, w, 3], dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            if direction == 'left':
                empty_img[i, j] = img[j, i]
                empty_img = empty_img[0:h, 0:w]

            elif direction == 'right':
                empty_img[i, j] = img[h - j, w - i]
                empty_img = empty_img[0:h, 0:w]

            else:
                # otherwise rotate 180 degrees
                empty_img[i, j] = img[h - i, w - j]
                empty_img = empty_img[0:h, 0:w]

    image_name = image_path.split('/')[-1].replace('.jpg', '')

    cv2.imwrite('{}/{}{}.jpg'.format(PATH_TO_IMAGES, image_name, direction), empty_img)


def main():
    # get all image names
    images = glob.glob('/*.jpg'.format(PATH_TO_IMAGES))

    for image in images:
        rotate_image(image, 'right')


if __name__ == '__main__':
    main()
