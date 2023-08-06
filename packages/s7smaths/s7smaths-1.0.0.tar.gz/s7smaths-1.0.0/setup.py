from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Synthesis math'
LONG_DESCRIPTION = 'Library with utterly non-unique math methods for use hopefully nowhere'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="s7smaths", 
        version=VERSION,
        author="Pieter Rossouw",
        author_email="pieter@synthesis.co.za",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'math'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)