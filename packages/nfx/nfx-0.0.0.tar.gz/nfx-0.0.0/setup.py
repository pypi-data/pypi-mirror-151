from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="nfx",
    description="Neuro Flow Extended",
    author="Avnish Yadav",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
)
