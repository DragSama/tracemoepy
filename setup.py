import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("tracemoepy/__init__.py", "r") as f:
    import re

    version = re.search("__version__ = (\S+)", f.read()).group(1)

setuptools.setup(
    name="tracemoepy",
    version=version,
    description="Trace.moe python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DragSama/tracemoepy",
    download_url="https://github.com/DragSama/tracemoepy/releases",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "aiohttp[speedups]", "attrify"],
    python_requires=">=3.6",
)
