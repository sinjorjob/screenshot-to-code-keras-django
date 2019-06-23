from django.conf import settings
from django.conf.urls.static import static
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from nltk.translate.bleu_score import sentence_bleu,corpus_bleu
from tqdm import tqdm
from os import listdir
from app1.compiler.classes.Compiler import *
from .config import *

import numpy as np
import h5py as h5py
import subprocess
import glob
import os
import tensorflow as tf


class ScreenShot():

    def __init__(self):
        self.max_length = 48
        self.is_empty(PNG_PATH)
        self.is_empty(CODE_PATH)
        self.is_empty(FEATUR_PATH)
        
    
    # ファイルを読み込んで文字列を返す
    def load_doc(self, filename):
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text
        

    def load_data(self):
        text = []
        images = []
        all_filenames = glob.glob(FEATUR_PATH + "\\*")
        all_filenames.sort()
        print((all_filenames)[-2:])
        for filename in (all_filenames)[-2:]:
            if filename[-3:] == "npz":
                image = np.load(filename)
                images.append(image['features'])
            
            else:
                # Bootstrap tokenをロードして開始タグと終了タグでラップ
                syntax = '<START> ' + self.load_doc(filename) + ' <END>'
                # Sすべての単語を1つのスペースで区切る
                syntax = ' '.join(syntax.split())
                # 各コンマの後にスペースを追加
                syntax = syntax.replace(',', ' ,')
                text.append(syntax)
        images = np.array(images, dtype=float)
        return images, text
    
    def create_gui(self,file_name):
        cmd = 'python manage.py create_gui' + " " + file_name
        print("cmd=",cmd)
        print("current_dir=", os.getcwd())
        os.chdir(settings.BASE_DIR)
        rc_code = subprocess.call(cmd, shell=True)
        return rc_code


    def create_npz(self):
        cmd = 'python manage.py create_npz'
        os.chdir(settings.BASE_DIR)
        rc_code = subprocess.call(cmd, shell=True)
        return rc_code


    # 語彙を作成するための関数を初期化
    def init_token(self):
        tokenizer = Tokenizer(filters='', split=" ", lower=False)
        # 語録の生成
        tokenizer.fit_on_texts([self.load_doc(MODEL_PATH + r"\bootstrap.vocab")])
        return tokenizer


    def load_model(self):
        json_file = open(MODEL_PATH + r"\model.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(MODEL_PATH + r"\weights.h5")
        print("Loaded model from disk")
        graph = tf.get_default_graph()
        return loaded_model, graph

    # word Indexを単語に変換する。
    def word_for_id(self, integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    # 画像の説明文を生成する
    def generate_desc(self, model, tokenizer, photo, max_length, graph):
        photo = np.array([photo])
        # 生成プロセスをシードする
        in_text = '<START> '
        # シーケンスの全長にわたって反復する
        print('\nPrediction---->\n\n<START> ', end='')
        for i in range(150):
            # 整数エンコード入力シーケンス
            sequence = tokenizer.texts_to_sequences([in_text])[0]
            # 入力データをPaddingする。
            sequence = pad_sequences([sequence], maxlen=max_length)
            #  next wordを予測
            with graph.as_default():
                yhat = model.predict([photo, sequence], verbose=0)
                # 確率を整数に変換
                yhat = np.argmax(yhat)
                # 整数を単語に写像する
                word = self.word_for_id(yhat, tokenizer)
                # 単語をマッピングできない場合は停止
                if word is None:
                    break
                # 次の単語を生成するための入力として追加
                in_text += word + ' '
                # シーケンスの終わりを予測したら停止
                print(word + ' ', end='')
                if word == '<END>':
                    break
        return in_text

    # モデルのスキルを評価する
    def evaluate_model(self, model, texts, photos, tokenizer, max_length, graph):
        actual, predicted = list(), list()
        for i in range(len(texts)):
            yhat = self.generate_desc(model, tokenizer, photos[i], max_length, graph)
            # Actualと予測
            print('\n\nReal---->\n\n' + texts[i])
            actual.append([texts[i].split()])
            predicted.append(yhat.split())
            # BLEUスコアを計算する
            bleu = corpus_bleu(actual, predicted)
            return bleu, actual, predicted
            

    def generate_html(self):
        # トークンをHTMLとcssにコンパイルします。
        dsl_path = "compiler/assets/web-dsl-mapping.json"
        compiler = Compiler(dsl_path)
        compiled_website = compiler.compile(predicted[0], 'index.html')
        return compiled_website
    

    def output_html(self, compiled_website):
        with open(os.path.join(HTML_PATH, "auto_create.html"), 'wb') as file:
            file.write(compiled_website.encode('utf-8'))
    

    def remove_files(self, target_dir):
        file_list = glob.glob(target_dir + "\\*")
        for file in file_list:
            os.remove(file)


    def is_empty(self, directory):
        if os.listdir(directory):
            self.remove_files(directory)










