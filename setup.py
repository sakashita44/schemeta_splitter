# setup.py
from setuptools import setup, find_packages

# バージョン情報を読み込む
version = {}
with open("schemeta_splitter/__version__.py") as fp:
    exec(fp.read(), version)

setup(
    name="schemeta_splitter",
    version=version["__version__"],
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "schemeta_splitter=schemeta_splitter.cli:main",
        ],
    },
)
