from setuptools import find_packages, setup

setup(
    name='discord_limits',
    packages=find_packages(include=['discord_limits']),
    version='0.0.1',
    description='Make requests API requests to Discord without having to worry about ratelimits.',
    author='ninjafella',
    license='MIT',
    install_requires=['aiolimiter==1.0.0', 'aiohttp==3.8.1']
)