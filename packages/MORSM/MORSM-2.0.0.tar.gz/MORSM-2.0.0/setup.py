import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
install_requires = [
    'numpy',
    'matplotlib.pyplot',
    'os',
    'sys',
    'argparse',
    'glob'
    'math'
    'logging',
    ]
    
    
setuptools.setup(
    name="MORSM",
    version="2.0.0",
    author="almog_blaer",
    author_email="blaer@post.bgu.ac.il",
    description="moment-rate oriented slip distribution for SW4 Seismic Waves simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["MOR-SM", "seismology", "SW4","EEW", "GMM"],
    url="https://github.com/ABlaer/MOR-SM",
    install_requires=install_requires,
    packages=setuptools.find_packages(),   
    license="GPL"
 
)
