python -m venv tortoise-venv
call .\tortoise-venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
python -m pip install -r ./requirements.txt
python setup.py install
deactivate
pause