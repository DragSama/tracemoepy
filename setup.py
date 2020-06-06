import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytracemoe",
    packagaes = ['pytracemoe'],
    version="0.2",
    description="Trace.moe python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DragSama/pytracemoe",
    download_url = 'https://github.com/DragSama/pytracemoe/archive/v0.2.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent"
    ],
    install_requires = [
        "requests"
    ],
    python_requires='>=3.6'
)
