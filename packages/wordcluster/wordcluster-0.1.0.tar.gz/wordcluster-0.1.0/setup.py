from pathlib import Path

from setuptools import setup

readme = Path(__file__).parent.joinpath('README.md')
if readme.exists():
    with readme.open() as f:
        long_description = f.read()
else:
    long_description = '-'

setup(
    name='wordcluster',
    version='0.1.0',
    description='A algoirthm for clustering similar words in a list',
    long_description=long_description,
    python_requires='>=3.6',
    packages=[
        'wordcluster',
    ],
    author='Dr. Suat ATAN',
    author_email='suatatan@gmail.com',
    url='',
    license='MIT',
    install_requires=[],
)
