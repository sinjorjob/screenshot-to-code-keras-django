from django.shortcuts import render
from django.views import generic
from .forms import DocumentForm
from .models import Document
from .utils import ScreenShot
from .config import *
from django.conf import settings
from app1.compiler.classes.Compiler import *
from keras import backend as K
import shutil
import os
import glob
import shutil, os
import glob


class UploadView(generic.FormView):
    form_class = DocumentForm
    template_name = 'app1/model_form_upload.html'

    def form_valid(self, form):
        K.clear_session()
        ss = ScreenShot()
        form.save()
        file_name = self.request.FILES['document'].name
        try:
            tokenizer =  ss.init_token()
            ss.create_gui(file_name)
            shutil.move(os.path.join(PNG_PATH, file_name), os.path.join(CODE_PATH ,file_name))
            ss.create_npz()
            file_list = glob.glob(CODE_PATH + "\\*")
            for file in file_list:
                os.remove(file)
            train_features, texts = ss.load_data()
            loaded_model, graph = ss.load_model()
            _, _, predicted = ss.evaluate_model(loaded_model, texts, train_features, tokenizer, ss.max_length, graph)
            compiler = Compiler(DSL_PATH)
            compiled_website = compiler.compile(predicted[0], TEMPLATE_HTML)
            ss.output_html(compiled_website)
            ss.remove_files(FEATUR_PATH)
            message = "Processing ended normally."
            context = {
                'message': message,
                'PREDICTED_HTML': PREDICTED_HTML,
                'compiled_website':compiled_website,}
            return render(self.request, 'app1/complete.html', context)
        except Exception as e:
            err_args ="Error:" + str(e.args)
            err_message ="message:" + str(e)
            context = {
                'err_args': err_args,
                'err_message': err_message,}
            return render(self.request, 'app1/complete.html', context)


    def form_invalid(self, form):
        return render(self.request, 'app1/model_form_upload.html', {'form': form})


