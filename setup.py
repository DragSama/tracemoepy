import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tracemoepy",
    packagaes = ['tracemoepy'],
    version="0.4",
    description="Trace.moe python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DragSama/tracemoepy",
    download_url = 'https://github.com/DragSama/tracemoepy/releases',
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
