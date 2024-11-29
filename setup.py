
from setuptools import setup, find_packages

setup(
    name='schemeta_splitter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'schemeta_splitter=schemeta_splitter.cli:main',
        ],
    },
)
