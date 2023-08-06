from setuptools import setup, find_packages
from sys import platform

pycoco = 'pycocotools' if platform=='linux' else 'pycocotools-windows'

print(pycoco)

setup(
    name='yolo_as_one',
    version='0.6.4',
    license='MIT',
    author="Bramwel Ochieng",
    author_email='bramwelochieng@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ochi96/yolo_as_one',
    keywords='yolox yolor yolov5 installation inferencing',
    install_requires=[
        'scikit-learn',
        'wheel',
        'numpy',
        'torch>=1.7.0',
        'opencv_python',
        'loguru',
        'scikit-image',
        'tqdm',
        'torchvision',
        'Pillow',
        'thop',
        'ninja',
        'tabulate',
        'tensorboard',
        'PyYAML>=5.3.1',
        'pandas>=1.1.4',
        'seaborn>=0.11.0',
        'thop',
        'requests>=2.23.0',
        'matplotlib>=3.2.2',
        pycoco,
        'gdown',
        'pytorch_wavelet'
      ],

    scripts=[
        './src/installation_scripts/yolor_installation.sh',
        './src/installation_scripts/yolox_installation.sh',
        './src/installation_scripts/yolov5_installation.sh',
        './src/installation_scripts/yolor_installation.bat',
        './src/installation_scripts/yolox_installation.bat',
        './src/installation_scripts/yolov5_installation.bat',
        './src/inference_scripts/yolor_inferencing.sh',
        './src/inference_scripts/yolox_inferencing.sh',
        './src/inference_scripts/yolov5_inferencing.sh',
        './src/inference_scripts/yolor_inferencing.bat',
        './src/inference_scripts/yolox_inferencing.bat',
        './src/inference_scripts/yolov5_inferencing.bat',

    ]
)