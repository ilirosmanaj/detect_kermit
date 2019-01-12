# from imageai.Detection import VideoObjectDetection
# import os
#
# import json
# import h5py
#
# # def fix_layer0(filename, batch_input_shape, dtype):
# #     with h5py.File(filename, 'r+') as f:
# #         model_config = json.loads(f.attrs['model_config'].decode('utf-8'))
# #         layer0 = model_config['config'][0]['config']
# #         layer0['batch_input_shape'] = batch_input_shape
# #         layer0['dtype'] = dtype
# #         f.attrs['model_config'] = json.dumps(model_config).encode('utf-8')
# #
# # # Example
# # fix_layer0('../data/images/models/kermit_klassifier.h5', [None, 64, 64], 'float32')
#
# execution_path = os.getcwd()
#
# detector = VideoObjectDetection()
# detector.setModelTypeAsYOLOv3()
# detector.setModelPath( os.path.join(execution_path , "../data/images/models/kermit_klassifier.h5"))
# detector.loadModel()
#
# video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join( execution_path, "../data/Muppets-02-01-01.avi"),
#                                 output_file_path=os.path.join(execution_path, "../data/muppets")
#                                 , frames_per_second=1, log_progress=True)
# print(video_path)

from imageai.Prediction import ImagePrediction
import os

execution_path = os.getcwd()

prediction = ImagePrediction()
# prediction.loadModel()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "kermit_klassifier.h5"))
prediction.loadModel()

# predictions, probabilities = prediction.predictImage(os.path.join(execution_path, "1.jpg"), result_count=5 )
# for eachPrediction, eachProbability in zip(predictions, probabilities):
#     print(eachPrediction , " : " , eachProbability)