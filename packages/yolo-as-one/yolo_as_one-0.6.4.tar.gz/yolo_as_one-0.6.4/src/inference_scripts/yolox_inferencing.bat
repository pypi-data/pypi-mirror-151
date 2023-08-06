@echo off
cd yolox

echo What kind of media is this?
set /p file_type="Type input: "


if %file_type%=="webcam" (
python tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth --path %1 --conf 0.25 --nms 0.45 --tsize 640 --save_result --device cpu --output %2 
) else (

python tools/demo.py %file_type% -f exps/default/yolox_s.py -c ./weights/yolox_s.pth --path %1 --conf 0.25 --nms 0.45 --tsize 640 --save_result --device cpu --output %2
)