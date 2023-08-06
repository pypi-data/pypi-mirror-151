from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.9'
DESCRIPTION = 'This Library tell about your mental health from a sentence. Like are you stressed or not ?'

with open('requirement.txt','r') as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="mentalHealth",
    version=VERSION,
    author="Ujjwal Kar",
    url="https://github.com/Mental-Health-Montitoring-with-AI/mentalHealth",
    author_email="ujjwalkar21@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = required,
    packages=find_packages(),
    package_data={
        'mentalHealth': ['svc_linear.pk','TfIdf_Vectorizer.pk'],
    },
    include_package_data=True,
    keywords=['Natural Language Processing'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    py_modules=['mentalHealth'],
)
