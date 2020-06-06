import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DragSama", # Replace with your own username
    version="0.1",
    author="DragSama",
    description="Trace.moe python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DragSama/pytracemoe",
    download_url = 'https://github.com/DragSama/pytracemoe/archive/v0.1.tar.gz'
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3),
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
