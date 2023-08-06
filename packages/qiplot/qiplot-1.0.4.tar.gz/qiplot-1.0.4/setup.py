from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
setup(
    name='qiplot',     # Name of the package. This is what people will be installing
    version='1.0.4',     # Version. Usually if you are not planning on making any major changes after this 1.0.0 is a good way to go.
    description='Graphs in 1D and 2D',     # Short description
    license='MIT',  
    maintainer='steche',
    long_description=long_description,     # This just makes your README.md the description shown on pypi
    long_description_content_type='text/markdown',
    maintainer_email='schecchi@gmx.com',
    #include_package_data=True,     # If you have extra (non .py) data this should be set to True
    entry_points={'console_scripts': ['qi=qiplot.plotdada:main', 'q2=qiplot.imageroi:main']},
    packages=find_packages(include=('qiplot', 'qiplot.*')),     # Where to look for the python package
    install_requires=[     # All Requirements
        'numpy',
        'pyqtgraph','PyQt5','matplotlib','h5py'
    ],
)
