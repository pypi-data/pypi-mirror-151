cd yolor

python detect.py --source %1 --cfg cfg/yolor_p6.cfg --weights ./weights/yolor_p6.pt --conf 0.25 --img-size 1280 --device cpu --output %2