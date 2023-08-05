from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datagen-tech",
    version="1.0.2",
    description="Datagen SDK",
    long_description_content_type='text/markdown',
    long_description=long_description,
    license="Apache License 2.0",
    author="Datagen Technologies Ltd.",
    url="https://datagen.tech/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "dependency-injector",
        "marshmallow-dataclass==8.5.3",
        "matplotlib==3.4.3",
        "numpy==1.22",
        "scipy==1.7.2",
        "pillow==8.3.2",
        "tqdm==4.62.3",
        "opencv-python==4.5.3.56",
        "jupyter==1.0.0",
        "Deprecated==1.2.13"
    ],
)
