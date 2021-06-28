@echo off

cd /D %~dp0

set INPUT=%1
set OUTPUT=test.binvox

python3 test.py -- %INPUT% %OUTPUT%

@pause