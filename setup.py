from setuptools import setup, find_packages

setup(name='dotcolors',
      version='0.1',
      description='manage Xresources colors from dotshare.it',
      url='http://github.com/jakhead/dotcolors',
      author='Chase Franklin',
      author_email='jakhead@gmail.com',
      packages = ['dotcolors'],
      py_modules = ['dotcolors'],
      license='MIT',
      install_requires=[
          'BeautifulSoup',
          'progressbar',
          'docopts'
          ],
      entry_points={
          'console_scripts':
          ['dotcolors = dotcolors.cli:main'
       ]}
     )
