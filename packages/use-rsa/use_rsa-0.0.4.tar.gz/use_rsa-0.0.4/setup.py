from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'encrypte your message'
LONG_DESCRIPTION = 'encrypte your message'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="use_rsa", 
        version=VERSION,
        author="Andriatina Ranaivoson",
        author_email="andriatina@aims.ac.za",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        #scripts=['dokr'],
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'rsa'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)