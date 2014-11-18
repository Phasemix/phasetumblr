from setuptools import setup

setup(name='phasetumblr',
      version='0.1',
      description='All the posts from a tumblr blog in a python list. ',
      url='http://github.com/phasemix/phasetumblr',
      author='Roberto Allende',
      author_email='rallende@gmail.com',
      license='Apache 2.0',
      packages=['phasetumblr'],
      install_requires = ["pytumblr", "phasepersist"],
      zip_safe=False)