from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='CreateAPI',
    version='0.0.9',
    description='A very simple API creator',
    long_description=open('README.txt').read(),
    url='',
    author='oren',
    author_email='orennadle@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='api-creator CreateAPI api-maker make-api api create-api create',
    packages=find_packages(),
    install_requires=['Flask']
)