# Copyright (c) 2022-2027 Starfive
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This package provides a Python module to control the GPIO on a Starfive.
"""

from setuptools import setup, Extension

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.8',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(name             = 'Starfive.GPIO',
      version          = '1.2.2',
      author           = 'Starfive',
      author_email     = 'Starfive.shanghai@starfivetech.com',
      description      = 'A module to control Starfive GPIO ports',
      long_description = open('README.txt').read() + open('CHANGELOG.txt').read(),
      license          = 'MIT',
      keywords         = 'Starfive GPIO',
      url              = 'http://gitlab.starfivetech.com/product1/oftware-ae/visionfive-python-gpio/starfive_gpio',
      classifiers      = classifiers,
      packages         = ['Starfive','Starfive.GPIO'],
      ext_modules      = [
      						Extension('Starfive._GPIO', ['source/py_gpio.c', 'source/c_gpio.c', 'source/py_constants.c', 'source/gpio-utils.c', 'source/py_sense.c', 'source/SHTC3_dev.c'],
									  extra_compile_args=['-D_GNU_SOURCE']
      								 )
      					 ]
      )
