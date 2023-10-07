from setuptools import setup, find_packages

setup(
    name='pygame-truly-centered-button',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
    author='Melvin Chen',
    author_email='melvinchen610@gmail.com',
    description='A Pygame button library that fixes text-centering',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mchen610/pygame-truly-centered-button',
)