@echo off

REM (2) 특정 파이썬 가상환경이 있다면 활성화 (옵션)
call crol\Scripts\activate.bat

REM (3) 메인 파이썬 스크립트 실행
python ajou_crol.py

REM (4) 작업 완료 후 화면을 잠깐 유지하고 싶다면
pause
