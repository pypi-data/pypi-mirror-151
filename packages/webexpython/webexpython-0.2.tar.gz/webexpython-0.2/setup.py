from setuptools import find_packages, setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='webexpython',
    packages=find_packages(where="src"),
    version='0.2',
    description='Empty',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Josh Kittle - josh.kittle@gmail.com',
    license='MIT',
    install_requires=['requests'],
    setup_requires=[],
    package_dir={"": "src"},
    python_requires=">=3.10",
)