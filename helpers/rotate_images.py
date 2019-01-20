import glob
from typing import Optional

from utils import print_progress
from PIL import Image

PATH_TO_IMAGES = '../data/images/train/kermit/kermit-train-images'


def rotate_image(image_path: str, direction: Optional[str]):
    image = Image.open(image_path)

    if direction == 'right':
        rotated = image.rotate(90)
    elif direction == 'left':
        rotated = image.rotate(-90)
    else:
        rotated = image.rotate(180)

    image_name = image_path.split('/')[-1].replace('.jpg', '')
    rotated.save('{}/{}{}.jpg'.format(PATH_TO_IMAGES, image_name, direction))


def main():
    # get all image names
    images = glob.glob('{}/*.jpg'.format(PATH_TO_IMAGES))

    for i, image in enumerate(images):
        rotate_image(image, 'right')
        rotate_image(image, 'left')
        rotate_image(image)
        print_progress((i + 1) / len(images))

    print('\nRotated {} images'.format(len(images)))


if __name__ == '__main__':
    main()
