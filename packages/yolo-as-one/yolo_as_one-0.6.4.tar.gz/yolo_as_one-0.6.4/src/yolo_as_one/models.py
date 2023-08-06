
import argparse
from subprocess import call
from sys import platform

model_names = ['yolox', 'yolor', 'yolov5']

def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--model_name', default='None')
    return parse.parse_args()


def install_models(model_name):
    if model_name in model_names:
        if platform == "linux" or platform == "linux2":
            call(f"{model_name}_installation.sh", shell=True)
        elif platform == "win32":
            call(f"{model_name}_installation.bat", shell=True)
        else:
            print('Operating Sytem unsupported')
    elif model_name=='all':
        for model_item in model_names:
            if platform == "linux" or platform == "linux2":
                call(f"{model_item}_installation.sh", shell=True)
            elif platform == "win32":
                call(f"{model_item}_installation.bat", shell=True)
            else:
                print('Operating Sytem unsupported')
    else:
        print('model currently unavailable')
    pass

def run_models(args):
    if args.model_name in model_names:
        if platform == "linux" or platform == "linux2":
            call(f"{args.model_name}_inferencing.sh {args.source} {args.save_dir}", shell=True)
        elif platform == "win32":
            call(f"{args.model_name}_inferencing.bat {args.source} {args.save_dir}", shell=True)
        else:
            print('Operating Sytem unsupported')
    else:
        print('model currently unavailable')
    pass


if __name__=='__main__':
    args = parse_args()
    install_models(args.model_name)
