python -m venv tortoise-venv
call .\tortoise-venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio torch-directml==0.1.13.1.dev230119
python -m pip install -r ./requirements.txt
python setup.py install
deactivate
pause