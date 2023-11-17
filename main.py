import numpy as np
import archiveUtils
from EncryptionAlgorithms.PartiallyHE import elGamal, paillier, RSA
from EncryptionAlgorithms.SomeWhatHE import BGV, GM
from EncryptionAlgorithms.FullyHE import CKKS_Bootstrapping, BFV

def main(printing:bool):
    resultASCII,result = archiveUtils.returnArchiveASCII("Files/1paragraph")
    '''print("---- result Paillier -----")
    print(resultASCII)
    print("---- result -------")
    print(result)'''
    print("------- Partially homomorphic encryption -------")

    
    #resultPaillierEnc,resultPaillierDec = paillier.execute(resultASCII,True)

    #resultRSAEnc,resultRSADec = RSA.execute(result, printing)

    #resultelGamalEnc,resultelGamalDec = elGamal.execute(resultASCII, printing)
    
    #resultBGVEnc, resultBGVDec = BGV.execute(resultASCII)

    #resultCKKSEnc, resultCKKSdec, resultSimilarity = CKKS.execute(resultASCII, True)

    #CKKS_Bootstrapping.execute(resultASCII,True)
    
    #BFV.execute(resultASCII,True)
    #testGM = [123,345]
    GM.execute(resultASCII, True)

if __name__ == "__main__":
    main(True)
