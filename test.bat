@echo off

cd /D %~dp0

set INPUT=%1
set DIMS=%2

python3 test.py -- %INPUT% %DIMS%

@pause