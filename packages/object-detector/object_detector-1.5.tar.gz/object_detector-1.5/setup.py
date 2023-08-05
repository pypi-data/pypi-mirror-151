from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.5'
DESCRIPTION = 'Using this library you can detect objects from a video, images, with few lines of code'

with open('requirement.txt','r') as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="object_detector",
    version=VERSION,
    author="Ujjwal Kar",
    url="https://github.com/ujjwalkar0/object_detector",
    author_email="ujjwalkar21@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = required,
    keywords=['YoLo','Object Detector','Artificial Intelligence'],
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    py_modules=['object_detector'],
)
