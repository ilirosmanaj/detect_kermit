from imageai.Prediction.Custom import CustomImagePrediction
import os


def predict_image(image_name: str, prediction: CustomImagePrediction, execution_path: str):
    """Predicts a given image with the supplied prediction model"""
    print('\nPredicting the {} image'.format(image_name))
    # results = []

    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, image_name), result_count=5)
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        # results.add((eachPrediction,eachProbability))
        print('     {} : {}'.format(eachPrediction, eachProbability))

    print('')


def main():
    execution_path = os.getcwd()

    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()

    # pass the correct model name (model name is changed in each run)
    prediction.setModelPath(os.path.join(execution_path, 'data/images/models/model_ex-015_acc-0.602679.h5'))
    prediction.setJsonPath(os.path.join(execution_path, 'data/images/json/model_class.json'))
    prediction.loadModel(num_objects=2)

    # TODO: later add support for multiple images/video prediction
    # predict_image(image_name='kermit_4.jpg', prediction=prediction, execution_path=execution_path)
    # predict_image(image_name='kermit_5.jpg', prediction=prediction, execution_path=execution_path)
    for i in range(1,4):
        predict_image(image_name = '{}.jpg'.format(i),prediction = prediction, execution_path = execution_path)


if __name__ == '__main__':
    main()