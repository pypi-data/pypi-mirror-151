import setuptools
import pathlib


setuptools.setup(
    name='ninjax',
    version='0.1.0',
    description='Simple and general state handling in JAX',
    url='http://github.com/danijar/ninjax',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['ninjax'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
