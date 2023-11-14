import numpy as np
import archiveUtils
from EncryptionAlgorithms.PartiallyHE import elGamal, paillier, RSA
from EncryptionAlgorithms.SomeWhatHE import BGV
from EncryptionAlgorithms.FullyHE.CKKS import CKKSEncoder

def main(printing:bool):
    resultASCII,result = archiveUtils.returnArchiveASCII("Files/1paragraph")
    '''print("---- result Paillier -----")
    print(resultASCII)
    print("---- result -------")
    print(result)'''
    print("------- Partially homomorphic encryption -------")
    
    '''
    resultPaillierEnc,resultPaillierDec = paillier.execute(resultPaillier)
    print(resultPaillierDec)
    asciiedPaillier = archiveUtils.retrieveValuesFromASCII(resultPaillierDec)
    print(asciiedPaillier)'''

    #resultRSAEnc,resultRSADec = RSA.execute(result, printing)

    #resultelGamalEnc,resultelGamalDec = elGamal.execute(resultASCII, printing)
    
    #resultBGVEnc, resultBGVDec = BGV.execute(resultASCII)

    #resultCKKSEnc, resultCKKSDec = CKKS.execute(resultASCII, True)

    CKKSEncoder.execute(np.array(resultASCII), True)
    #CKKS.execute(resultASCII, True)

if __name__ == "__main__":
    main(True)
