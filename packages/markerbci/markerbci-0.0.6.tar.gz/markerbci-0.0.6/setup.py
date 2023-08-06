import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="markerbci",
    version="0.0.6",
    author="Simon Kojima",
    author_email="simon.kojima@outlook.com",
    description="Handling marker devices for brain-computer interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonkojima/markerbci-python",
    project_urls={
        "Bug Tracker": "https://github.com/simonkojima/markerbci-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=2.6",
)