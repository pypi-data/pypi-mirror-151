# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, European Space Agency & European Southern Observatory (ESA/ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
# 
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
# 
#      * Neither the name of the European Space Agency, European Southern 
#        Observatory nor the names of its contributors may be used to endorse or 
#        promote products derived from this software without specific prior 
#        written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ESA/ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

"""
Install script for libxmp.
"""
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

import sys

setup(
	name='djangoplicity-python-avm-library',
	version='1.0.3',
	description="Python AVM Library for working with Astronomy Visualization Metadata.",
	long_description=open('README.rst').read(),
	author='Amit Kapadia',
	author_email='akapad@gmail.com',
	url='https://github.com/djangoplicity/djangoplicity-python-avm-library',
	download_url='https://github.com/djangoplicity/djangoplicity-python-avm-library/archive/refs/tags/1.0.3.tar.gz',
	license='New BSD License',
	packages=['libavm'],
)