# Standard library imports
from setuptools import setup, find_packages

setup(
    name='vproces',
    include_package_data=True,
    packages = find_packages(),
    version='0.0.8',
    author='Wojciech A',
    author_email='wa@gmail.com',
    license='LICENSE.txt',
    description='An awesome package that does something',
    long_description=open('README.md').read(),
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=[
        'opencv-python>=4.5.5'
    ]
)
