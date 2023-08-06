import numpy as np
import random


def ensemble_average(N_sample, N_candi, N_mol, X, file_X_avg, Int_lam, file_P_avg):
  '''
  This function generates N_sample no. of ensemble averaged structures & properties, 
  by randomly taking N_candi no. of molecules from N_mol and averaging them.
  '''

    X_avg = []
    P_avg = []
    print('Ensemble averaging')
    for i in range(N_sample):
        indices=list(random.sample(range(0, N_mol), N_candi))
        sum_X = 0.0
        sum_P = 0.0
        for j in range(N_candi):
            sum_X = sum_X + X[indices[j]]
            sum_P = sum_P + Int_lam[indices[j]]
        avg_X = sum_X/N_candi
        avg_P = sum_P/N_candi

        X_avg.append(avg_X)
        P_avg.append(avg_P)
        if np.mod(i,100) == 0:
            print(i, 'samples done out of', N_sample)
    P_avg = np.array(P_avg, dtype=float)
    np.save(file_X_avg, X_avg)
    np.save(file_P_avg, P_avg)

    return  X_avg, P_avg
