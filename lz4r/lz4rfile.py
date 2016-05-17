import sys, os
import tarfile
from StringIO import StringIO

import lz4tools
import lz4f

# remove {"lz4" : "lz4open"} from OPEN_METH due to ReadError Bug in lz4tools
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

        # check whether the uncompressed file is a directory/tar or not
        # untar it if it's a tar
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
        :type string: name      - name of file to compress
        :type bool:   overwrite - overwrite destination
        :type string: outname   - name for compressed file, not required.
                                  Default will be '.'.join([name, 'lz4r'])
        Generic compress method for a file. Adds .lz4r to original file name for
        output, unless outname is provided.

        ***NOTE*** No longer uses compressFrame. This is now large file safe!
        It will now read the input in 64Kb chunks.
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
        :type string: Name   - the name of the dir to tar
        :type bool:   overwrite - overwrite destination
        Generic compress method for creating .tar.lz4 from a dir.

        ***WARNING*** Currently uses StringIO object until lz4file supports write.
        Avoid using for large directories, it will consume quite a bit of RAM.
        """
        if not outname:
            outname = '.'.join([name.rstrip('/'), 'lz4r'])
        if not os.path.exists(name):
            print('Unable to locate the directory to compress.')
            return

        # if the dir is huge and use a buff to hold the dir, the size of buff
        # will become huge, which is unacceptable. So load it into a tar file
        # firstly, then read this tar file and compress it with lz4
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


