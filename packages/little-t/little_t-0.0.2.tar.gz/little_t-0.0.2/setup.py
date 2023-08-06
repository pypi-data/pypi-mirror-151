from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'little-t binaries'
LONG_DESCRIPTION = 'files and packages needed for little-t'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="little_t",
    version=VERSION,
    author="Alex McCune",
    author_email="alexmccune1224@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where="little_t_package"),
    install_requires=[],  # add any additional packages that
    package_dir={"":"little_t_package"},
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
