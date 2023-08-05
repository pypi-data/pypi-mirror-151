cd yolox

python tools/demo.py image -f exps/default/yolox_s.py -c ./weights/yolox_s.pth --path assets/dog.jpg --conf 0.25 --nms 0.45 --tsize 640 --save_result --device [cpu/gpu]

python3 tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth  --conf 0.3 --nms 0.65 --tsize 640 --device cpu
