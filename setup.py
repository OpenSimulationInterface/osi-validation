"""
Setup module of OSI Validation Software
"""
import glob
import sys
import os
import setuptools

AUTHOR = "BMW AG"


if __name__ == "__main__":
    with open("README.md", "r") as fh:
        README = fh.read()

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    data_files_path = os.path.join(
        "lib", f"python{python_version}", "site-packages", "rules"
    )

    setuptools.setup(
        name="osivalidator",
        version="1.1.0",
        author=AUTHOR,
        description="Validator for OSI messages",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/OpenSimulationInterface/osi-validation",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved",
            "Operating System :: OS Independent",
        ],
        data_files=[
            (
                "open-simulation-interface",
                glob.glob("open-simulation-interface/*.proto"),
            ),
            (
                data_files_path,
                glob.glob("rules/*.yml"),
            ),
        ],
        include_package_data=True,
        install_requires=[
            "tqdm",
            "tabulate",
            "ruamel.yaml",
            "defusedxml",
            "iso3166",
            "protobuf>=3.20.1",
            "open-simulation-interface",
        ],
        # https://stackoverflow.com/a/54701434
        #dependency_links=[
        #    "git+https://github.com/OpenSimulationInterface/open-simulation-interface.git@master#egg=open-simulation-interface",
        #],
        entry_points={
            "console_scripts": ["osivalidator=osivalidator.osi_general_validator:main"],
        },
    )
