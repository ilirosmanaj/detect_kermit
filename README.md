# Kermit Detection Repo
![Kermit wanted](https://github.com/ilirosmanaj/detect_kermit/blob/master/readme_images/kermit_wanted.jpg)

This repository contains the code for detecting Kermit (the frog) from
`The Muppets` TV show. It uses [ImageAI](https://github.com/OlafenwaMoses/ImageAI) python library
(which is build on top of tensorflow object detection API).


# Setup

**Note**: The following has only been tested on linux operating systems,
so not sure whether it will work for other operation systems.

Install the needed packaged via pip, by running:

```bash
pip install -r requirements.txt
```

Since models are growing quite big, we are using Git LFS (Large File Storage). In order to install
it do:

osX:
```
brew install git-lfs
```

ubuntu:
```
sudo apt-get install git-lfs
```


## General steps:

* Get images from `The Muppets show` videos
* Use frames from episode 1 and 2 as training set
    * Those frames are divided in two classes: `kermit` and `no-kermit`
* Use frames from episode 3 as validation set
* Enrich Kermit images by:
    * rotating images (left, right and 180 degrees)
    * downloading some more Kermit images from google
* Enrich non kermit images by adding non kermit images (e.g. green frogs, humans, nature etc)

## Running

### Get images from videos

In order to get the frames as images from video, run the following:

```bash
cd helpers
python convert_vid2image.py
```

**Note:** Due to large file sizes the video files are not checked in in the repository, rather 
only the corresponding script

### Rotate Images

In order to learn the model better, its a common practice to enrich the dataset with 
rotated images so that it sees things in different perspectives.

To do this run the following:

```bash
cd helpers
python rotate_images.py
```

This will store all images in the same path with `right` or `left` postfix.

### Download from google

As part of enriching the data, model is supplied with some images outside of 
the served images from the video. What was done here is using the `google_images_download` which
can be found [here](https://github.com/hardikvasa/google-images-download)  


```bash
cd helpers
python downloads_from_google.py
```

### Training the model

Since ImageAI library was used, we have trained the CustomImagePrediction model (which uses Resnets as 
network model type).

To train the model, run the following:

```bash
python imageai_build_model.py
```

**Note:** Please make sure that the folder structure for images is as following:

* data
    * images
        * train
            * kermit
            * no-kermit
        * test
            * kermit
            * no-kermit
            
 After model is trained, the corresponding trained model is stored in `h5` format under 
 the `data/images/models/model_name.h5`

### Run predictions on the model

After having the model trained, you can run predictions on it using two different input formats
(either a video or image).

To run predictions on an image, run the following:

```bash
python kermit_model_evaluation.py -t [one of image or video] -f [file path to image - comma 
separated string supported as well, or path to video]
```

E.g. Predicting an image:

```bash
python kermit_model_evaluation.py -t image -f kermit.jpeg

Predicting the kermit.jpeg image
 kermit: 99.87 no-kermit: 0.13

```
...which is awesome.

Same can be done for a video:

```bash
python kermit_model_evaluation.py -t video -f MuppetsEpisode3.avi
```

This will get all the frames in 1 second interval from the video, store them under `tmp` (for now 
named as episode3_results) folder as jpegs with a banner on top of the image that shows the prediction result 
for each frame. 

## Example run:

Since episode3 was used as validation set, the results and corresponding predictions for it 
are stored under `episode3_results` directory. Check it out or see a part of classification

![Episode3 Results](https://github.com/ilirosmanaj/detect_kermit/blob/master/readme_images/episode3.gif)



## Troubleshooting:

pip distribution of tensorflow does not work for osX, so it can be installed via the url
using the following command:

```
python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
```

Sometimes tensorflow gpu might complain about limited number of running devices. 
To fix it, just set the `CUDA_VISIBLE_DEVICES` environment variable as follows:

```
export CUDA_VISIBLE_DEVICES=''
```