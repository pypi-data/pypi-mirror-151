. linvenv/bin/activate

cd yolox

echo What kind of media is this?
read file_type

if [$file_type==webcam]
then
    python3 tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth --path $1 --conf 0.25 --nms 0.45 --tsize 640 --save_result --device cpu --output $2
else
    python3 tools/demo.py $file_type -f exps/default/yolox_s.py -c ./weights/yolox_s.pth --path $1 --conf 0.25 --nms 0.45 --tsize 640 --save_result --device cpu --output $2
fi




# python3 tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth  --conf 0.3 --nms 0.65 --tsize 640 --device cpu

# python3 tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth  --conf 0.3 --nms 0.65 --tsize 640 --device cpu --save_result
