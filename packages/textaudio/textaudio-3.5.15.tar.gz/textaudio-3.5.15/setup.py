from distutils.core import setup
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='textaudio',
      version='3.5.15',
      description='convert Text to audio file',
       long_description = long_description,
      author='Ankan Saha',
      author_email='admin@ankansaha.in',
      url='https://github.com/AnkanSaha/textaudio',
      packages=setuptools.find_packages()
     )
install_requires = ['gtts','playsound','pyautogui']
