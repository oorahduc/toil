import os
from setuptools import setup, Command


class Clean(Command):
    description = "Cleans up the build files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            os.system('rm -rf build dist toil.egg-info')
            print("Removed build, dist, and toil.egg-info directories")
        except Exception as e:
            raise e


setup(
    name='toil',
    version='0.1.0',
    description='a python task organizer/progress keeper. a clone of nodejs taskbook',
    author='chris kimmel',
    author_email='chriskimmel@gmail.com',
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'toil = toil:main'
        ],
    },
    py_modules=['toil'],
    packages=['toil_lib'],
    install_requires=['cement', 'python-dateutil'],
    cmdclass={
        'clean': Clean
    }
)
