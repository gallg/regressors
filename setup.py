from setuptools import setup, find_packages

requirements = [
    'numpy>=1.6.1',
    'scipy>=0.9',
    'matplotlib',
    'scikit-learn>=0.17',
    'statsmodels>=0.6.1',
    'seaborn',
    'pandas',
]

VERSION = '0.0.4'
DESCRIPTION = 'regressors'
LONG_DESCRIPTION = 'Easy utilities for fitting various regressors, extracting stats, and making relevant plots'

# Setting up
setup(
    name="regressors",
    version=VERSION,
    author="PNI Lab (Predictive NeuroImaging Laboratory)",
    author_email="<giuseppe.gallitto@uk-essen.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python', 'machine learning', 'statistics'],
    classifiers=[]
)
