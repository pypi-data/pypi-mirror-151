from setuptools import find_namespace_packages, setup

AUTHOR = 'Samuel Reyes'
LICENSE = 'MIT'
DESCRIPTION = 'Aquí debes incluir una descripción corta de la librería' 
with open('README.md') as f:
        LONG_DESCRIPTION = f.read()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'regex'
      ]

setup(
    name='validateFieldData',
    version='0.4.1',
    packages=find_namespace_packages(),
    py_modules=['validateFieldData'],
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    
)
