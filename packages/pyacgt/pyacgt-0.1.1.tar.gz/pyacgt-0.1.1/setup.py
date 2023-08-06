import setuptools
from setuptools import find_packages, setup
import os, platform


if platform.system() == "Linux":
    ACME_EXE = r"pyACME/bin/acme"
elif platform.system() == "Windows":
    ACME_EXE = r"pyACME/bin/acme.exe"
elif platform.system() == "Darwin":
    raise NotImplementedError("Mac OSX Not yet supported.") 


def readme()->str:
    """Where the README file is."""
    with open(r'README.md','r+') as f:
        return f.read()


setup(
    name='pyacgt',
    version='0.1.1',
    description='Python interface to ACME',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/nick5435/pyacgt',
    author='Nick Meyer',
    author_email='nmeyer5435@gmail.com',
    license='GPLv3+',
    packages=find_packages(),
    zip_safe=False,
    setup_requires=[],
    install_requires=['typing>=3.7.0, <4;python_version <="3.8" ', 'typing_extensions>=4.0.0, <5; python_version <= "3.11"'
    ],
    extras_require={
        'dev': [],
    },
    python_requires='>=3.7.0',
    include_package_data=True,
    package_data={
        'bin': [ACME_EXE]
    },
    keywords="mathematics group-theory andrews-curtis",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ]
    )