cd yolox

python tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth  --conf 0.3 --nms 0.65 --tsize 640 --device cpu
