from setuptools import setup

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
    install_requires=['cement', 'python-dateutil']
)