from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read().replace('# ', '').replace('\n', ' | ')

setup(
    name='congress_voting',
    description='Scrape and Examine Congressional Voting Data',
    author_email='gregawert@gmail.com',
    url={'github': 'https://github.com/gregwert/congress_voting'},
    version='0.0.1dev',
    python_requires='>=3.6',
    package_dir={'': 'congress_voting'},
    packages=find_packages('congress_voting'),
    install_requires=[
        'pandas>=0.24.0',
        'numpy>=1.17.0'
    ],
    long_description=long_description,
)
