
set BASE_DIR=<set django project folder>
set BAT_DIR=%BASE_DIR%\app1\model

cd /d %BAT_DIR%
python convert_imgs_to_arrays.py ../code ../features

set CMD_RC=%ERRORLEVEL%

exit /b %CMD_RC%

