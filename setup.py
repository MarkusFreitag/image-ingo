from setuptools import setup, find_packages

setup(name='image-ingo',
      version='0.1.1',
      description='Python3 script for sorting images.',
      author='Markus Freitag',
      author_email='fmarkus@mailbox.org',
      license='MIT',
      packages=find_packages(),
      install_requires=['click', 'exifread'],
      entry_points={
          'console_scripts': ['image-ingo=image_ingo.commands:cli'],
          },
      zip_safe=False)
