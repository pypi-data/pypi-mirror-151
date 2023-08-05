import setuptools

with open("README_pip.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EA_framework-OhGreat",
    version="0.2.7",
    author="Dimitrios Ieronymakis",
    author_email="dimitris.ieronymakis@gmail.com",
    description="A framework for applying evolutionary algorithms to generic optimization problems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OhGreat/evolutionary_algorithms",
    project_urls={
        "Bug Tracker": "https://github.com/OhGreat/evolutionary_algorithms/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.21.5",
        "matplotlib>=3.5.0",
    ],
)