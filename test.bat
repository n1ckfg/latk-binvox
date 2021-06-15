@echo off

cd /D %~dp0

set INPUT=%1
set OUTPUT=test.latk

python test.py -- %INPUT% %OUTPUT%

@pause