import setuptools

author = 'Altran Germany / BMW'
    
if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()



    setuptools.setup(
        name="osivalidator",
        version="0.0.1",
        author=author,
        description="Validator for OSI messages",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ainar/osi-validation",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
        install_requires=[
            'iso3166',
            'pyyaml',
            'asteval',
            'sphinx_rtd_theme',
            'recommonmark',
            'open-simulation-interface',
        ],
        dependency_links=[
            'git+https://github.com/OpenSimulationInterface/open-simulation-interface.git@master#egg=open-simulation-interface',
        ],
        entry_points = {
            'console_scripts': ['osivalidator=osivalidator.osi_general_validator:main'],
        }
    )
