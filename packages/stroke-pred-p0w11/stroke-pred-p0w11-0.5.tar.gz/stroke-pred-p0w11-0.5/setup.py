
from setuptools import setup, find_packages

setup(
    name='stroke-pred-p0w11',
    version='0.5',
    license='MIT',
    author="Patrick Saade",
    author_email='patrick_saade@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Isaacgv/stroke_heart_prediction',
    keywords='stroke prediction project',
    install_requires=[
          'scikit-learn',
          'pandas',
          'numpy',
      ],

)