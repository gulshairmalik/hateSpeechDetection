# Hate Speech Detection
A system that detects hate speech from an Urdu language audio file or Urdu text.

## Pre-Requisites
To run the project make sure you have following things installed:

- Nodejs & npm
  - [Install Nodejs & NPM (Linux)](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04) 

- Nodemon
  - Install nodemon globally with this command ```sudo npm i -g nodemon```

- FFMPEG
  - [Install ffmpeg (Linux)](https://linuxize.com/post/how-to-install-ffmpeg-on-ubuntu-18-04/) 
  
- YTDL
  - [Install YTDL](https://www.npmjs.com/package/ytdl) 

- SOX
  - Install SOX on linux with ```sudo apt-get install sox libsox-fmt-all```

- Python3 & pip
  - [Install Python3 & PIP (Linux)](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/)

- Python Django Framework
  - [Install Python Django Framework](https://docs.djangoproject.com/en/2.2/topics/install/#installing-official-release)
  - [Install Django cors-headers](https://pypi.org/project/django-cors-headers/)

- Python3 Libraries:
  **Install Libraries with** ```pip install LIBRARY_NAME```
  - gensim
  - pyfasttext==0.4.6
  - xlsxwriter==1.1.2
  - numpy==1.15.4
  - scikit-learn==0.20
  - pandas==0.24.1
  - python-crfsuite
  - nltk
  - scipy

## Running the App Locally
To run the app on your localhost, take following steps:

- Open the terminal in project root directory and run ```python3 ./hateSpeechModel/mywebapp/manage.py runserver``` to run python server

- Open another terminal in project root directory and run ```export GOOGLE_APPLICATION_CREDENTIALS="PATH_TO_GOOGLE_API.json"```
  - **Note:** You must have Google-API .json file to run this command

- After running above command, run ```nodemon``` to run the NodeJs server locally.
