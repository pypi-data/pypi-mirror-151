from setuptools import find_packages, setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='bwnormalize',
    version='0.0.1',
    description='Converter of dates and monetary values ​for frontend and backend return',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Bruno Ramos',
    author_email='brunoramos90@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='dates, currency',
    packages=find_packages(),
    install_requires=['']
)
