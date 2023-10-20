## requirements(if not working automatically individually install all libraries from requirements.txt)
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

## run venueguard(If you have webcam, can do num_cams=2 and it will automatically display 2 sources)
python Base_GUI.py --num_cams=1