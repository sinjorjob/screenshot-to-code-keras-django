# screenshot-to-code-keras-django



Made Screen-shot-to-code a Django app.

【demo】
https://youtu.be/wajrQF6N0gI


Operation has been confirmed in python 3.6, windows 10 environment.
Works only with Windows.


# Outline of construction procedure

１．Install python (3.6 or more) in advance.

２．Download the project with git

```
git clone https://github.com/sinjorjob/screenshot-to-code-keras-django.git
```

※ Or download from the upper right "Clone or Download"-> "Download ZIP" of git

３．Execute setup command from command prompt

windows

```
cd screenshot-to-code-keras-django-master\pix2code
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

※It does not work on MacOS / Linux.

４．Preparation of models, weight files, etc.

Create pix2code.h5 according to the procedure of "Train the model:" at https://github.com/tonybeltramelli/pix2code, and place it in "\ pix2code \ app1 \ bin \ pix2code2.h5".

# train on top of pretrained weights
./train.py ../datasets/web/training_features ../bin 1 ../bin/pix2code.h5

Place model.json and weights.h5 in pix2code \ app1 \ model.

Download the learned models and weights file from　https://www.floydhub.com/emilwallner/datasets/imagetocode, or Create a learning model according to  http://github.com/emilwallner/Screenshot-to-code/tree/master/Bootstrap.

Reference URL 
https://github.com/emilwallner/Screenshot-to-code

５．change bat file path

target file

screenshot-to-code-keras-django/pix2code/app1/management/commands/create_npz.py  
screenshot-to-code-keras-django/pix2code/app1/management/commands/create_gui.bat  

```
set BASE_DIR=<set django project folder>
```
change BASE_DIR to djnago project root path.

example

```
set BASE_DIR=C:\screenshot-to-code-keras-django-master\pix2code
```



６．Start development server

windows

```
python manage.py runserver
```


URL

```
http://127.0.0.1:8000/pix2code/upload/
```

