from setuptools import setup

setup(
    name='cameo_threshold',
    version='1.0.0',
    description='large performance increase',
    release_notes='',
    url='https://github.com/bohachu/cameo_threshold',
    author='JC Wang',
    author_email='jcxgtcw@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_threshold'],
    install_requires=[
        'fastparquet==0.8.1',
        'numpy==1.22.3',
        'pandas==1.4.2',
        'pyarrow==7.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)