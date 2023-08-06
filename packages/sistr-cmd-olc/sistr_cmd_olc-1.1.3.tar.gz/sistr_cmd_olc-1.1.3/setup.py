from setuptools import setup, find_packages
from sistr.version import __version__

classifiers = """
Development Status :: 4 - Beta
Environment :: Console
License :: OSI Approved :: Apache Software License
Intended Audience :: Science/Research
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Operating System :: POSIX :: Linux
""".strip().split('\n')

setup(
    name='sistr_cmd_olc',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/phac-nml/sistr_cmd',
    license='Apache 2.0',
    author='Peter Kruczkiewicz',
    author_email='peter.kruczkiewicz@gmail.com',
    description=('Serovar predictions from Salmonella whole-genome sequence assemblies by determination of antigen gene'
                 'and cgMLST gene alleles using BLAST. Mash MinHash can also be used for serovar prediction.'),
    keywords='Salmonella serotyping genotyping cgMLST BLAST Mash MinHash',
    classifiers=classifiers,
    package_dir={'sistr': 'sistr'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'sistr = sistr.sistr_cmd:main',
            'sistr_init = sistr.sistr_cmd:setup_sistr_dbs'
        ],
    },
)
