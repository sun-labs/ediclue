from setuptools import setup, find_packages

setup(
    name='ediclue',
    version="0.0.8",
    description='An open source parser for EDIEL data',
    url='https://github.com/sun-labs/ediclue',
    author='Sun Labs Nordic AB',
    author_email='code@sunlabs.se',
    license='Free for non-commercial use',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        # Pick your license as you wish (should match "license" above)
        'License :: Free for non-commercial use',

        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'Topic :: Communications',

        'Environment :: Console'
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',


        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='ediel energy parser consumption svk sunlabs edifact',
    packages=find_packages(),
    install_requires=[]
)