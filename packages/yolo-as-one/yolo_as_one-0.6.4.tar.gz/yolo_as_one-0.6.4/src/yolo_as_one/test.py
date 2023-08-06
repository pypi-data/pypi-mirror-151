
from models import run_models, install_models

from argparse import ArgumentParser
from subprocess import call
from sys import platform


install_models('all')

# def run_model(args):
#     call(f"/media/bram/PlayField/Projects/Freelancing/Ritesh_YOLO/yolo_as_one/src/inference_scripts/{args.model_name}.sh {args.source} {args.save_dir}", shell=True)

#     pass

# if __name__ == "__main__":

#     parser = ArgumentParser()
#     parser.add_argument("--model_name", type=str,
#                         help="specify the model to test")
#     parser.add_argument("--source",
#                         help="specify the source: image, video or webcam=0",
#                         default='image')
#     parser.add_argument("--save_dir",type=str, help="results are saved here",
#                         default=False)
#     parser.add_argument('--view_img', action='store_true', help='show results',
#                         default=False)
#     args = parser.parse_args()
#     # demo code
#     run_model(args)

