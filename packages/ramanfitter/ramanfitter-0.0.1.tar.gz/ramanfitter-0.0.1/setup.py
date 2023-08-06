from setuptools import setup, find_packages
import codecs
import os

here                = os.path.abspath( os.path.dirname( __file__ ) )

with codecs.open( os.path.join( here, "README.md" ) ) as fh:

    long_description    = "\n" + fh.read()

VERSION             = '0.0.1'
DESCRIPTION         = 'A Raman peak finder and model fitter'
LONG_DESCRIPTION    = 'A module that automatically finds peaks in Raman data and uses those peaks to fit a Lorentzian, Gaussian, or Voigt model'

setup(
    name                            = 'ramanfitter',
    version                         = VERSION,
    author                          = 'John Ferrier',
    author_email                    = "<jo.ferrier@northeastern.edu>",
    description                     = DESCRIPTION,
    long_description_content_type   = "text/markdown",
    long_description                = long_description,
    packages                        = find_packages(),
    install_requires                = [ 'numpy', 'scipy', 'matplotlib', 'lmfit' ],
    keywords                        = [ 'python', 'raman', 'fitter', 'raman fitter', 'lorentzian', 'gaussian', 'voigt' ],
    classifiers                     = [
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Intended Audience :: Science/Research",
        "Natural Language :: English"
    ]
)