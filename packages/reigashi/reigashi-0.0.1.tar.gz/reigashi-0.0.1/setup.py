import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reigashi",
    version="0.0.1",
    author="amenota",
    author_email="leizd@outlook.com",
    description="some utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amenota/reigashi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
