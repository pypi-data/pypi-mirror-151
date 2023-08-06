# coding utf8
import setuptools
from toolbiox.versions import get_versions

setuptools.setup(
    name="ToolBiox",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="a biological toolkit for genome assembly, annotation and analysis that we have accumulated from our bioinformatics work",
    url="https://github.com/SouthernCD/ToolBiox",

    packages=setuptools.find_packages(),

    install_requires=[
        "bcbio-gff>=0.6.6",
        "biopython>=1.76",
        "deepTools>=3.5.0",
        "interlap>=0.2.6",
        "matplotlib>=3.5.0",
        "networkx>=2.4",
        "numpy>=1.18.1",
        "pandas>=1.0.1",
        "pyfaidx>=0.5.5.2",
        "pysam>=0.15.2",
        "retry>=0.9.2",
        "scikit-bio>=0.5.6",
        "scikit-learn>=0.22.2.post1",
        "scipy>=1.4.1",
        "seaborn>=0.11.2",
    ],

    python_requires='>=3.5',

)
