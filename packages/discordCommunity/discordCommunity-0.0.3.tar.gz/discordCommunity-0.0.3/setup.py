from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='discordCommunity',
    version='0.0.3',
    description='A Community Nuker library for discord.py',
    long_description=open('README.txt').read(),
    url='',
    author='DestructiveLone',
    author_email='lambo.blac123@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='discord',
    packages=find_packages(),
    install_requires=['requests']
)