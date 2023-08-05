
from setuptools import setup, find_packages

setup(
    name = 'ine_tugesto_somenergia',
    include_package_data = True,
    packages = ['ine_tugesto_somenergia'],   
    package_data = {'ine_tugesto_somenergia': ['csv/*.csv']},
    version = '1.0.0.1',
    description = 'Translates INE to Tugesto ids',
    author='Som Energia',
    author_email='info@somenergia.coop',
    license='MIT',
    url='https://github.com/som-energia/ine_tugesto',
    classifiers = [
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent'],
    )
