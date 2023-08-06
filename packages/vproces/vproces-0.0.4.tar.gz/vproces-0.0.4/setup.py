# Standard library imports
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "README.md").read_text()

setup(
    name='vproces',
    include_package_data=True,
    packages = find_packages(),
    version='0.0.4',
    author='Wojciech A',
    author_email='wa@gmail.com',
    license='LICENSE.txt',
    description='An awesome package that does something',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=[
        'opencv-python>4.5.5'
    ]
)
