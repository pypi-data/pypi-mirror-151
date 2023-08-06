import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="welcome_chi_chi",
    version="0.0.1",
    author="autn",
    description="An introduction from Chi Chi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["welcome_chi_chi"],
    package_dir={'':'welcome_chi_chi'},
    install_requires=[]
)
