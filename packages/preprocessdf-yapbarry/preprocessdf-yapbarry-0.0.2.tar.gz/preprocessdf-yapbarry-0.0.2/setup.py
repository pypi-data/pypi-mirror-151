from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="preprocessdf-yapbarry",
    version="0.0.2",
    description="handy functions to preprocess your dataframes or numpy arrays",
    py_modules=["preprocessdf"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    # url="https://github.com/judy2k/helloworld",
    author="Barry Yap",
    author_email="yapweiminbarry@gmail.com",

    install_requires=[
        "scikit-learn ~= 1.0.2",
    ],

    extras_require={
        "dev": [
            "pytest >= 7.1.2",
            "check-manifest",
            "twine",
        ],
    },
)
