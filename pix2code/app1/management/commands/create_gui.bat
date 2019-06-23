

set BASE_DIR=<set django project folder>
set BAT_DIR=%BASE_DIR%\app1\model
set MEDIA_DIR=%BASE_DIR%\media\png
set FILE_PATH=%MEDIA_DIR%\%1

cd /d %BAT_DIR%
python sample.py ../bin pix2code2 %FILE_PATH% ../code 3
set CMD_RC=%ERRORLEVEL%


exit /b %CMD_RC%

