
git clone https://github.com/ochi96/yolox.git

cd yolox

python3 setup.py install

mkdir -p weights

# wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth -O ./weights/yolox_s.pth
gdown https://drive.google.com/uc?id=1q_f0fG0MnQ0JVEFkVoIXDZ2_KZ2oAcf8 -O ./weights/yolox_s.pth
