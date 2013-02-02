from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tabtomidi',
    version='0.1',
    description='Generate MIDI files from ASCII drum tablature',
    long_description=readme,
    author='Josh Rosen',
    author_email='rosenville@gmail.com',
    url='https://github.com/JoshRosen/tabtomidi',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
