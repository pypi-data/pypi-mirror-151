import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open("README.md", "r") as f:
    long_description = f.read()

long_description_ = (here / 'README.md').read_text()

setuptools.setup(
    name="statistical_methods",
    version="0.0.2",
    author="nbooth99",
    author_email="nathan_booth@outlook.com",
    description="Functions for Statistical Analysis",
    long_description_content_type="text/markdown",
    long_description=long_description_,
    python_requires=">=3.6",
    setup_requires =[],
    tests_require=[],
    install_requires=[],
    packages=setuptools.find_packages(),
    package_dir={'statistical_methods': 'statistical_methods'},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],

)