import argparse
import asyncio
from copy import deepcopy
from typing import Union

import os
import cv2

import numpy as np
from imageai.Prediction.Custom import CustomImagePrediction

from helpers.utils import print_progress, gather_dict

EXECUTION_PATH = os.getcwd()


async def predict_image(image_name: Union[str, np.ndarray], model: CustomImagePrediction, input_type: str) -> str:
    """Predicts a given image with the supplied prediction model"""
    if input_type == 'file':
        print('\nPredicting the {} image'.format(image_name))

    image = os.path.join(EXECUTION_PATH, image_name) if isinstance(image_name, str) else image_name

    predictions, probabilities = model.predictImage(image, result_count=2, input_type=input_type)

    representation = ''
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        representation += '     {} : {}'.format(eachPrediction, eachProbability)

    return representation


async def predict_video(video_path: str, model: CustomImagePrediction):
    cap = cv2.VideoCapture(video_path)
    VIDEO_PLAYING_SPEED = 2
    VIDEO_DURATION_IN_SECONDS = int(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)) + 1

    print('Predicting video frames...')

    counter = 0
    tasks = {}
    # read all frames and run predictions on them

    while cap.isOpened():
        # set position to only read full seconds
        cap.set(cv2.CAP_PROP_POS_MSEC, (counter * 1000))
        ret, frame = cap.read()

        tasks[counter] = asyncio.ensure_future(predict_image(deepcopy(frame), model, input_type='array'))
        counter += 1
        print_progress(counter / VIDEO_DURATION_IN_SECONDS)

        if counter >= VIDEO_DURATION_IN_SECONDS:
            break

    print('\nGetting predictions foreach frame from the model')
    results = await gather_dict(tasks)

    print('\nStarting video output....')

    # show video with the given results
    cap = cv2.VideoCapture(video_path)
    counter = 0
    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_MSEC, counter)
        ret, frame = cap.read()
        cv2.imshow('Test', frame)

        index = int(counter/1000)
        res = results.get(index)

        if res:
            print(results[index])
            results.pop(index)

        counter += 1

        if cv2.waitKey(VIDEO_PLAYING_SPEED) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


async def main(file_type: str, files: str):
    model = CustomImagePrediction()
    model.setModelTypeAsResNet()

    model.setModelPath(os.path.join(EXECUTION_PATH, 'data/images/models/model_ex-100_acc-0.875000.h5'))
    model.setJsonPath(os.path.join(EXECUTION_PATH, 'data/images/json/model_class.json'))
    model.loadModel(num_objects=2)  # number of objects on your trained model

    if file_type == 'image':
        for image in files.split(','):
            await predict_image(image_name=image, model=model, input_type='file')
    else:
        await predict_video(video_path=files, model=model)


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--file_type', '-t', help='Inputs file type', type=str, default='video')
    arguments.add_argument('--files', '-f', help='File path. Comma separated images accepted if type image',
                           type=str, default='Muppets.avi')
    args = arguments.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.file_type, args.files))
    loop.close()
