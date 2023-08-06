from setuptools import setup, find_packages


setup(
    name='mono-diff',
    version='0.1.4',
    license='MIT',
    author="Ran Sasportas",
    author_email='ran729@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ran729/mono',
    keywords='mono',
    install_requires=['fire == 0.4.0','tenacity == 7.0.0']
)