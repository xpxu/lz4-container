#!/usr/bin/env python
import os
import unittest
from lz4r.lz4rfile import Lz4rFile


class test_lz4r_file(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.system('touch testfile')
        os.system("echo 'hello world' > testfile")
        os.system('mkdir testdir')
        os.system('cp testfile testdir')

    @classmethod
    def tearDownClass(cls):
        os.system('rm -rf testdir')
        os.system("rm -rf testdir.lz4r")
        os.system('rm -rf testfile')
        os.system('rm -rf testfile.lz4r')

    def test_1_compressdir(self):
        Lz4rFile.compress('testdir')
        self.assertTrue(os.path.exists('testdir.lz4r'))

    def test_2_decompressdir(self):
        os.system('rm -rf testdir')
        Lz4rFile.decompress('testdir.lz4r')
        dircount = 1
        for root, dirs, files in os.walk('testdir'):
            dircount += len(dirs)
            dircount += len(files)
        self.assertEqual(dircount, 2)

    def test_1_compressfile(self):
        Lz4rFile.compress('testfile')
        self.assertTrue(os.path.exists('testfile.lz4r'))

    def test_2_decompressfile(self):
        os.remove('testfile')
        Lz4rFile.decompress('testfile.lz4r')
        with open('testfile') as f:
            self.assertTrue(f.read() == 'hello world\n')

if __name__ == '__main__':
    unittest.main()