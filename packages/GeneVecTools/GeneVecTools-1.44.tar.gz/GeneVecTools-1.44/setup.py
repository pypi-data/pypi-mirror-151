from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()
# long_description = (this_directory / "README.rst").read_text()

setup(
    name="GeneVecTools",
    version="1.44",
    license="danielum16license",
    author="Daniel Um",
    author_email="danielum.16@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/danielum16/SecondProject",
    keywords="example project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "scikit-learn",
        "pandas",
        "faiss-cpu",
        "numpy",
        "requests",
        # "io",
        "tensorflow",
        # "datetime",
        # "os",
        # "sys",
        "biopython",
        "pysam",
    ],
)
