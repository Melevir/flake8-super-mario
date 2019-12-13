from typing import Optional

from setuptools import setup, find_packages


package_name = 'flake8_super_mario'


def get_version() -> Optional[str]:
    with open('flake8_super_mario/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md') as f:
        return f.read()


setup(
    name=package_name,
    description='A flake8 plugin with super_mario specific validations',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Console',
        'Framework :: Flake8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='flake8',
    version=get_version(),
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=['setuptools'],
    entry_points={
        'flake8.extension': [
            'SME = flake8_super_mario.checker:SuperMarionChecker',
        ],
    },
    url='https://github.com/Melevir/flake8-super-mario',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
