from setuptools import setup, find_packages

setup(
    name='plp_eduplanner',
    version='0.0.1',
    packages=['plp_eduplanner'],
    description='PLP education planner',
    url='http://dvebukvy.ru/',
    author='xacce',
    install_requires=['django_mptt==0.8.6','django-autocomplete-light<=2.2.10']
)
