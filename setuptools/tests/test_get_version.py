# -*- coding: utf-8 -*-

"""Tests for setuptools.get_version()."""
import os
import codecs
import shutil
import tempfile

import pytest

from setuptools import __version__, get_version


def test_own_version():
    version = get_version('setup.cfg', field='current_version')

    # `setup.py egg_info` which is run in bootstrap.py during package
    # installation adds `.post` prefix to setuptools.__version__
    # which becomes different from 'setup.cfg` file

    # https://setuptools.readthedocs.io/en/latest/setuptools.html#egg-info

    assert __version__.startswith(version + '.post')


class TestFiles:
    def setup_method(self, method):
        self.tmpdir = tempfile.mkdtemp()

    def teardown_method(self, method):
        shutil.rmtree(self.tmpdir)

    def test_python_file(self):
        path = os.path.join(self.tmpdir, 'version.py')
        with open(path, 'w') as fp:
            fp.write('__version__ = "0.23beta"\n')

        version = get_version(path)
        assert version == '0.23beta'

    def test_non_utf8_python_file(self):
        path = os.path.join(self.tmpdir, 'russian.py')
        with open(path, 'wb') as fp:
            fp.write(u'# файл в русской кодировке\n\n'.encode('cp1251'))
            fp.write(u'__version__ = "17.0"\n'.encode('cp1251'))

        version = get_version(path)
        assert version == '17.0'

