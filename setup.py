"""
Setup module of OSI Validation Software
"""
import glob

import setuptools

AUTHOR = 'Altran Germany / BMW'

if __name__ == "__main__":
    with open("README.md", "r") as fh:
        README = fh.read()

    setuptools.setup(
        name="osivalidator",
        version="0.1a0",
        author=AUTHOR,
        description="Validator for OSI messages",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/OpenSimulationInterface/osi-validation",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved",
            "Operating System :: OS Independent",
        ],
        data_files=[
            ('open-simulation-interface',
             glob.glob('open-simulation-interface/*.proto')),
            ('proto2cpp', ['proto2cpp/proto2cpp.py']),
            ('requirements-osi-3',
             glob.glob('requirements-osi-3/*.yml'))
        ],
        include_package_data=True,
        install_requires=[
            'iso3166',
            'ruamel.yaml',
            'asteval',
            'sphinx_rtd_theme',
            'recommonmark',
            'open-simulation-interface',
            'doxygen-interface',
            'defusedxml',
            'colorama',
            'tabulate',
        ],
        dependency_links=[
            'git+https://github.com/OpenSimulationInterface/' +
            'open-simulation-interface.git' +
            '@master#egg=open-simulation-interface',
        ],
        entry_points={
            'console_scripts':
                ['osivalidator=osivalidator.osi_general_validator:main'],
        }
    )
