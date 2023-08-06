import setuptools, sys, os

with open(os.path.join(os.path.dirname(__file__), "errr", "__init__.py"), "r") as f:
    for line in f:
        if "__version__ = " in line:
            exec(line.strip())
            break

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='errr',
     version=__version__,
     author="Robin De Schepper",
     author_email="robingilbert.deschepper@unipv.it",
     description="Elegant detailed Python exceptions.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Helveg/errr",
     license='MIT',
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     extras_require={
        "dev": ["sphinx", "sphinx_rtd_theme"]
     }
 )
