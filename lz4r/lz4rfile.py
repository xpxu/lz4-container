#coding=utf-8
import sys, os
import tarfile
from StringIO import StringIO

import lz4tools
import lz4f

# remove {"lz4" : "lz4open"} from OPEN_METH due to ReadError Bug in lz4tools
# open issue in github:　https://github.com/darkdragn/lz4tools/issues/13
tarfile.TarFile.OPEN_METH = {
    "tar": "taropen",  # uncompressed tar
    "gz": "gzopen",  # gzip compressed tar
    "bz2": "bz2open",  # bzip2 compressed tar
}


class Lz4rFile():

    @classmethod
    def compress(cls, name, overwrite=False, outname=None, prefs=None):
        if os.path.isfile(name):
            cls.compressFile(name, overwrite, outname, prefs)
        elif os.path.isdir(name):
            cls.compressDir(name, overwrite, outname, prefs)

    @classmethod
    def decompress(cls, name, overwrite=False, outname=None, prefs=None):
        """
        Be careful with directory which has many files
        """
        if not outname:
            outname = name.replace('.lz4r', '')
            if outname == name:
                print(''.join(['File does not contain .lz4r extension. ',
                               'Please provide outname.']))
                return
            if os.path.exists(outname) and not overwrite:
                print(''.join(['Output file exists! Please authorize overwrite or',
                               ' specify a different outfile name.']))
        infile = lz4tools.Lz4File.open(name)

        # uncompress the file into disk directly instead of memory
        writeOut = open(outname, 'wb')
        for blk in infile.blkDict.values():
            out = infile.read_block(blk=blk)
            writeOut.write(out)
            writeOut.flush()
        writeOut.close()

        # check whether the uncompressed file is a directory/tar or not．
        # untar it if it's a tar
        # [Note]: if the directory have many files, we can use tar.members = []
        # with loop to reduce memory usage. However, it will take more time
        # than use extractall directly.
        if tarfile.is_tarfile(outname):
            outpath = os.getcwd()
            tarname = outname + '.tar'
            os.rename(outname, tarname)
            tarobj = tarfile.open(tarname, "r")
            tarobj.extractall(path = outpath)
            tarobj.close()
            os.remove(tarname)

    @classmethod
    def compressFile(cls, name, overwrite=False, outname=None, prefs=None):
        """
        This is large file safe. It will now read the input in 64Kb chunks.
        """
        if not outname:
            outname = '.'.join([name, 'lz4r'])
        if os.path.exists(outname):
            if not overwrite:
                print('File Exists!')
                return
            print('Overwrite authorized')
        if not os.path.exists(name):
            print('Unable to locate the original file. Please check filename.')
            return
        cCtx = lz4f.createCompContext()
        header = lz4f.compressBegin(cCtx, prefs)
        with open(outname, 'wb') as out:
            out.write(header)
            with open(name, 'rb') as infile:
                while True:
                    decompData = infile.read((64*(1 << 10)))
                    if not decompData:
                        break
                    compData = lz4f.compressUpdate(decompData, cCtx)
                    out.write(compData)
                out.write(lz4f.compressEnd(cCtx))
            out.flush()
            out.close()
        lz4f.freeCompContext(cCtx)

    @classmethod
    def compressDir(cls, name, overwrite=None, outname=None, prefs=None):
        """
        Be careful with directory which has many files
        """
        if not outname:
            outname = '.'.join([name.rstrip('/'), 'lz4r'])
        if not os.path.exists(name):
            print('Unable to locate the directory to compress.')
            return

        # if the dir is huge and use a buff to hold the dir, the size of buff
        # will become huge, which is unacceptable. So load it into a tar file
        # firstly, then read this tar file and compress it with lz4.
        # Notes:
        # I guess it's better to use 'tar' command directly here because
        # tarfile is not good for python 2* when dealing with directory which
        # have many files. see http://stackoverflow.com/questions/21039974/
        # high-memory-usage-with-pythons-native-tarfile-lib
        tarname = name + '.tar'
        tar = tarfile.open(tarname, "w")
        tar.add(name)
        tar.close()

        cCtx = lz4f.createCompContext()
        header = lz4f.compressBegin(cCtx, prefs)
        with open(outname, 'wb') as out:
            out.write(header)
            with open(tarname, 'rb') as infile:
                while True:
                    decompData = infile.read((64*(1 << 10)))
                    if not decompData:
                        break
                    compData = lz4f.compressUpdate(decompData, cCtx)
                    out.write(compData)
                out.write(lz4f.compressEnd(cCtx))
            out.flush()
            out.close()
        lz4f.freeCompContext(cCtx)
        os.remove(tarname)


