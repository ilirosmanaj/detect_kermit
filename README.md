# Kermit Detection repo

This repository contains the code for detecting Kermit (the frog) from
the puppets tv show. It uses tensorflow object detection API.


# Installation and running

**Note**: The following has only been tested on osX, so not sure whether
it will work for other operation systems.

Install the needed packaged via pip, by running:

```bash
pip install -r requirements.txt
```

Sometimes installing tensorflow via pip does not work, so you
can manually download the distribution with:

```
python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
```

**Note**: this download tensorflow 1.12.0. Please adapt the url if you need
another version.


A lot (or the entire) procedure of setting up has been based on the accepted answert
at [this stackoverflow question](https://stackoverflow.com/questions/44973184/train-tensorflow-object-detection-on-own-dataset),
and also from [this article](https://towardsdatascience.com/how-to-train-your-own-object-detector-with-tensorflows-object-detector-api-bec72ecfe1d9).

The guy from the article also shared the source code (which is for Raccoon detector)
and that can be found [here](https://github.com/datitran/raccoon_dataset). The answer
from stackoverflow and this guy have used basically the same structure/steps.


## General steps:

### 1. Convert input to a format Tensorflow understands

Tensorflow works with a format called TFRecord (Tensorflow records). To convert
images to a this format, the steps [from this procedure](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/using_your_own_dataset.md) were used.

As described in the tutorial, here the Pascal VOOC format, which is an xml file that
contains each image (path, size etc) and the corresponding bounding box for the
class you are trying to detect. In order to generate those annotations, as suggested
by the guy on the article, the [LabelImg](https://github.com/tzutalin/labelImg) python
package was used.

**Note**: If LabelImg does not work, consider using [FIAT - Fast Image Annotation Tool](https://github.com/christopher5106/FastAnnotationTool)

The code that does this is under `helpers/create_annotations.py` script.

After creating the annotations (and surprisingly having the csv which contains all those info in one place - and looks
something like [this](https://github.com/datitran/raccoon_dataset/blob/master/data/raccoon_labels.csv)), then we have a script that just
randomly splits those data in train/test. That is under `helpers/split_train_test.py`

After creating the annotations, those can be used to create the tensorflow records as
described in the tensorflow models on [from this procedure](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/using_your_own_dataset.md),
or just try to copy the guy from article who did it [like this - which is quite similar](https://github.com/datitran/raccoon_dataset/blob/master/generate_tfrecord.py)

At this point, we should have all our labeled images in a format which is ready for
tensorflow object detection api to be used.

TODO: later, write some instructions on how to use scripts - or just put some docs on the script level

### 2. Create Pipeline (train model on the cloud)

### 3. Visualize

The above step 2 and 3 should not be that complicated, but what we are still not sure is how
to create a real time video detector...