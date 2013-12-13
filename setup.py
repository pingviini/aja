import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(name='aja',
      version='0.1.0',
      description='Deploy buildouts with ease.',
      long_description="%s\n%s" % (README, CHANGES),
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
      ],
      author='Jukka Ojaniemi',
      author_email='jukka.ojaniemi@gmail.com',
      url='https://github.com/pingviini/aja',
      keywords='deploy buildout',
      package_dir={"": "src"},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'docopt',
          'fabric',
          'zc.buildout',
          'pycrypto==2.6.1'
      ],
      extras_require={
          'docs': ['Sphinx']
      },
      entry_points={
          'console_scripts': ['aja=aja.main:main']
      },
      )
