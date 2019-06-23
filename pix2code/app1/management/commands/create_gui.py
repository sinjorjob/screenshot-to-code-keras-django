from django.core.management.base import BaseCommand
from datetime import datetime
from django.conf import settings

import subprocess
import os

bat_dir = os.path.join(settings.BASE_DIR, r'app1\management\commands\create_gui.bat')

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name')

    """ カスタムコマンド定義 """
    def handle(self, *args, **options):
        
        # ここに実行したい処理を書く
        file_name = options['file_name']
        cmd = (bat_dir, file_name)
        rc_code = subprocess.check_call(cmd, shell=True)
        if rc_code == 0:
            message = "OK"
        else:
            message = "NG"