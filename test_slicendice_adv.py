#!/usr/bin/env ccp4-python
# pytest-based CCP4 build verification tests
# Copyright (C) 2022 CCP4, Maria Fando


import pytest
import os
import shutil

@pytest.fixture(autouse=True) #return to test dir in case of test failure
def run_around_tests():
    
    curDir = os.getcwd()
    yield
    if os.getcwd() != curDir:
        os.chdir(curDir)

def test_slicendice2():
    import sys
    import subprocess

    if sys.platform.startswith("win"):
        executableName = 'slicendice.bat' # .bat for Windows
    else:
        executableName = 'slicendice'

    cexam = os.getenv('CEXAM')
    ccp4_scr = os.getenv('CCP4_SCR')

    assert cexam is not None
    assert ccp4_scr is not None
    assert os.path.exists(cexam)
    assert os.path.exists(ccp4_scr)

    cmd =['set -e']

    curDir = os.getcwd()
    os.chdir(ccp4_scr)


    outBaseName = ccp4_scr + os.sep + 'slicendice_0' + os.sep + 'output' + os.sep

    if os.path.exists(outBaseName):
        shutil.rmtree(ccp4_scr + os.sep + 'slicendice_0', ignore_errors=True) #delete output from previous run
    
    cmd = [executableName]
    cmd += ['-xyzin', cexam + os.sep + 'data' + os.sep + '7ocn_openfold_prediction.pdb']
    cmd += ['-xyz_source', 'alphafold']
    cmd += ['-max_splits', '3']
    cmd += ['-min_splits', '3']
    cmd += ['-hklin', cexam + os.sep + 'data' + os.sep + '7ocn.mtz']
    cmd += ['-seqin', cexam + os.sep + 'data' + os.sep + '7ocn.fasta']

    params = ''

    execProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    for param in params:
        execProcess.stdin.write(bytearray(param, 'utf-8'))
        execProcess.stdin.flush()
    execProcess.stdin.close()

    execSTDOUT = ''
    for line in execProcess.stdout:
        execSTDOUT += line.decode('utf-8')
    execProcess.stdout.close()

    exitCode = execProcess.wait()

    print(execSTDOUT)

    assert exitCode == 0 # exit code reports success
    assert os.path.exists(outBaseName + 'split_3_refmac.mtz')  # output file was created
    assert os.path.getsize(outBaseName + 'split_3_refmac.mtz') > 0 # output file has size more than zero
    assert os.path.exists(outBaseName + 'split_3_refmac.pdb')  # output file was created
    assert os.path.getsize(outBaseName + 'split_3_refmac.pdb') > 0 # output file has size more than zero

    os.chdir(curDir)



# if __name__ == "__main__":
#     print( 'slicendice2()')
#     test_slicendice2()