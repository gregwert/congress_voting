from setuptools import setup, find_packages

setup(
    name='congress_voting',
    description='Scrape and Examine Congressional Voting Data',
    author_email='gregawert@gmail.com',
    url={'github': 'https://github.com/gregwert/congress_voting'},
    version='0.1dev',
    python_requires='>=3.6',
    package_dir={'': 'congress_voting'},
    packages=find_packages(where='congress_voting'),
    install_requires=['pandas'],
    long_description=open('README.md').read(),
)
