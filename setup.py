import os.path
import setuptools


def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name='mkdocs-include',
    version='1.0.0',
    packages=['mkdocs_include'],
    url='https://github.com/nqkdev/mkdocs-include',
    license='Apache',
    author='Khanh Nguyen',
    author_email='qknguyendev@gmail.com',
    description='A mkdocs plugin that lets you include files or trees.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['mkdocs'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        'mkdocs.plugins': [
            'include = mkdocs_include:Include',
        ]
    },
)
