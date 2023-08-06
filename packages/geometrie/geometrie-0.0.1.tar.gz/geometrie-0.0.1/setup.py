import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()


setuptools.setup(
    name="geometrie",
    version="0.0.1",
    author="Sage Kataliko",
    description="Librarie pour le calcul des formes geometriques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    py_modules=["geometrie"],
    package_dir={'':'geometrie/src'},
    install_requires=[]
)