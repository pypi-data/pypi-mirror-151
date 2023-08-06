from setuptools import setup, find_packages

setup(
    name='dpp-token-api-lib',
    version='0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=open('README.md').read(),
    # install_requires=['numpy'],
    url='https://git.e-science.pl/kwazny_252716_dpp/kwazny252716_dpp_python_pip',
    author='Karol Ważny',
    author_email='kwazny_252716@e-science.pl'
)