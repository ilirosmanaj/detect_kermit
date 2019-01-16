import asyncio
from copy import deepcopy
from functools import wraps
from typing import Union

import click
import os
import cv2

import numpy as np
from imageai.Prediction.Custom import CustomImagePrediction

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

    print(representation)
    print('')

    return representation


async def predict_video(video_path: str, model: CustomImagePrediction):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        asyncio.create_task(predict_image(deepcopy(frame), model, input_type='array'))
        # res = predict_image(deepcopy(frame), model, input_type='array')
        title = 'test'
        cv2.imshow(title, frame)

        if cv2.waitKey(6) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


@click.command()
@click.option('--file_type', '-t', type=click.Choice(['image', 'video']), default='video', help='Inputs file type')
@click.option('--files', '-f', type=click.STRING, required=True, default='Muppets.avi',
              help='File path. Comma separated images accepted if type image')
async def main(file_type: str, files: str):
    model = CustomImagePrediction()
    model.setModelTypeAsResNet()

    # pass the correct model name (model name is changed in each run)
    model.setModelPath(os.path.join(EXECUTION_PATH, 'data/images/models/model_ex-100_acc-0.875000.h5'))
    model.setJsonPath(os.path.join(EXECUTION_PATH, 'data/images/json/model_class.json'))
    model.loadModel(num_objects=2)

    if file_type == 'image':
        for image in files.split(','):
            pass
            # predict_image(image_name=image, model=model, input_type='file')
    else:
        await predict_video(video_path=files, model=model)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
