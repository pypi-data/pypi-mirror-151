from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='go-deploy',
    version='0.1.0',
    include_package_data=False,
    url='https://github.com/geneontology/devops-deployment-scripts.git',
    author='Abdelilah Essiari',
    author_email='aessiari@lbl.gov',
    description='Provision using terraform and ansible',
    long_description=long_description,      
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],     
    python_requires='>=3.8.5',
    packages=find_packages(),    
    install_requires=[
       'pyyaml>=6.0', 
    ],
    entry_points={
       'console_scripts': [
              'go-deploy = go.deploy:main',
       ]
    },
)
