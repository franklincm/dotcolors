from setuptools import setup

setup(name='dotcolors',
      version='0.1',
      description='manage Xresources colors from dotshare.it',
      url='http://github.com/jakhead/dotcolors',
      author='Chase Franklin',
      author_email='jakhead@gmail.com',
      packages=['dotcolors'],
      license='MIT',
      install_requires=[
          'BeautifulSoup',
          'progressbar',
          'docopts'
          ],
      scripts=['bin/dotcolors'],
      zip_safe=False)
