import argparse
import asyncio
from typing import Union

import os
import cv2

import numpy as np
from imageai.Prediction.Custom import CustomImagePrediction

from helpers.utils import print_progress, gather_dict

EXECUTION_PATH = os.getcwd()


async def predict_image(image_name: Union[str, np.ndarray], model: CustomImagePrediction) -> str:
    """Predicts a given image with the supplied prediction model"""
    print('\nPredicting the {} image'.format(image_name))

    predictions, probabilities = model.predictImage(os.path.join(EXECUTION_PATH, image_name), result_count=2)

    representation = ''
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        representation += ' {0}: {1:.2f}'.format(eachPrediction, float(eachProbability))

    return representation


async def predict_video(video_path: str, model: CustomImagePrediction):
    cap = cv2.VideoCapture(video_path)
    VIDEO_DURATION_IN_SECONDS = int(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)) + 1
    # remove tmp images
    # os.system('rm -rf tmp')

    print('Gathering frames from the video...')

    counter = 0
    tasks = {}
    # read all frames and run predictions on them
    while cap.isOpened():
        # set position to only read full seconds
        cap.set(cv2.CAP_PROP_POS_MSEC, (counter * 1000))
        ret, frame = cap.read()

        if not ret:
            break

        # store the image and use that one for predicting
        image_name = 'tmp/test_frame{}.jpg'.format(counter)
        cv2.imwrite(image_name, frame)

        tasks[image_name] = asyncio.ensure_future(predict_image(image_name, model))
        counter += 1
        print_progress(counter / VIDEO_DURATION_IN_SECONDS)

    cap.release()
    cv2.destroyAllWindows()

    print('\nGetting predictions foreach frame from the model...')
    results = await gather_dict(tasks)


    print('\nWriting predictions on images....')

    for image_path in results.keys():
        print('\nWriting prediction for {}'.format(image_path))
        img = cv2.imread(image_path)
        cv2.putText(img, results[image_path], (130, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imwrite(image_path, img)

    print('\nDone....')


async def main(file_type: str, files: str):
    model = CustomImagePrediction()
    model.setModelTypeAsResNet()

    model.setModelPath(os.path.join(EXECUTION_PATH, 'data/images/models/kermit_finder.h5'))
    model.setJsonPath(os.path.join(EXECUTION_PATH, 'data/images/json/model_class.json'))
    model.loadModel(num_objects=2)  # number of objects on your trained model

    if file_type == 'image':
        for image in files.split(','):
            print(await predict_image(image_name=image, model=model))
    else:
        await predict_video(video_path=files, model=model)


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--file_type', '-t', help='Inputs file type', type=str, default='video')
    arguments.add_argument('--files', '-f', help='File path. Comma separated images accepted if type image',
                           type=str, default='MuppetsEpisode3.avi')
    args = arguments.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.file_type, args.files))
    loop.close()
