from django.conf import settings
import os

MODEL_PATH = os.path.join(settings.BASE_DIR, r'app1\model')
DSL_PATH = os.path.join(settings.BASE_DIR, r"app1\compiler\assets\web-dsl-mapping.json")
CODE_PATH = os.path.join(settings.BASE_DIR, r"app1\code")
PNG_PATH = os.path.join(settings.MEDIA_ROOT, r'png')
HTML_PATH = os.path.join(settings.MEDIA_ROOT, "html")
FEATUR_PATH = os.path.join(settings.BASE_DIR, r"app1\features")
TEMPLATE_HTML = os.path.join(settings.BASE_DIR, r"app1\model\index.html")
PREDICTED_HTML = "auto_create.html"
MAX_LENGTH = 48