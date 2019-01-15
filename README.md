# Kermit Detection repo

This repository contains the code for detecting Kermit (the frog) from
the puppets tv show. It uses [ImageAI](https://github.com/OlafenwaMoses/ImageAI) python library
(which is build on top of tensorflow object detection API).


# Installation and running

**Note**: The following has only been tested on linux operating systems,
so not sure whether it will work for other operation systems.

Install the needed packaged via pip, by running:

```bash
pip install -r requirements.txt
```

pip distribution of tensorflow does not work for osX, so it can be installed via the url
using the following command:

```
python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
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

* Get images from `The muppets show` videos
* Use frames from episode 1 and 2 as training set
    * Those frames are divided in two classes: `kermit` and `no-kermit`
* Use frames from episode 3 as testing set
* Enrich kermit images by:
    * rotating images
    * downloading some kermit images from google

Good to have:
    * some automated way of seeing results from evaluation the model