# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from SNR_ESTIMATION.MATCH_SIG import match_sig
from  formatConvert.wav_pcm import get_data_array
from commFunction import make_out_file


speechSection = [12, 15]
noiseSection = [0, 10]
FRAME_LEN = 960

def get_data_pairs(srcFile=None,testFile=None):
    """
    Parameters
    ----------
    srcFile
    testFile
    Returns
    -------
    """

    samples = int(match_sig(refFile=srcFile, testFile=testFile))

    dataSrc, fs, chn = get_data_array(srcFile)
    dataTest, fs2, chn2 = get_data_array(testFile)

    print(dataTest,dataSrc,samples)
    assert fs == fs2
    assert  chn2 == chn
    assert samples > 0

    dataTest = dataTest[samples:]
    M,N = len(dataSrc),len(dataTest)
    targetLen = min(M,N)
    return dataSrc[:targetLen],dataTest[:targetLen],fs,chn

if __name__ == '__main__':
    src = r'C:\Users\vcloud_avl\Documents\我的POPO\TestCase_07_bubble_25\speech_cn\mixFile_minus_6.wav'
    test = r'C:\Users\vcloud_avl\Documents\我的POPO\TestCase_07_bubble_25\speech_cn\mixDstFile_minus_6.wav'
    srcdata,dstdata,fs,chn = get_data_pairs(srcFile=src,testFile=test)
    make_out_file('src.wav',srcdata,fs,chn)
    make_out_file('dst.wav',dstdata,fs,chn)
