from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
    name='dlib2mediapipe',
    version='0.0.2',
    description='A Python package that allows developers to transition from Dlib to MediaPipe FaceMesh or convert Dlib projects to MediaPipe.',
    author= 'Rohit Thomas ,Avinash S Kurup ,Boby Chaitanya Villari',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['dlib to mediapipe ', 'dlib converter', 'dlib to mediapipe converter', 'face landmark detector'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['dlib2mediapipe'],
    package_dir={'':'src'},
    install_requires = [
        'opencv-python',
        'mediapipe',

    ]
)