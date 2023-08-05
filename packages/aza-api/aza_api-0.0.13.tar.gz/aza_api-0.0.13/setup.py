"""To push to pypit

python setup.py sdist
twine upload dist/*
"""
import setuptools

version = "0.0.13"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aza_api",
    version=f"{version}",
    author="Oscar Lundberg",
    author_email="lundberg.oscar@gmail.com",
    description="Package to fetch data from Avanza",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olundberg/aza_api",
    download_url=f"https://github.com/olundberg/aza_api/archive/refs/tags/v_{version}.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["webdriver-manager",
                      "selenium>=3.141.0",
                      ],
)
