import numpy as np
import qml
from qml.kernels import laplacian_kernel, gaussian_kernel



def single_kernel_sigma(N_sample, X, indices, kernel, typ):


    
    #D = np.zeros([N_sample,N_sample],dtype=float)

    #for i in range(N_sample):
    #    for j in range(N_sample):
    #        D[i,j] = np.sum(np.abs(X[indices[i]] - X[indices[j]]))
            
    D = []
    for i in range(0,N_sample-1):
        for j in range(i+1,N_sample):
            Dij = np.sum(np.abs(X[indices[i]] - X[indices[j]]))
            D.append(Dij)
            
    D=np.array(D,dtype=float)

    Dmax = np.max(D)
    Dmedian = np.median(D)

    if kernel == 'laplacian':
        if typ == 'max':
            opt_sigma = Dmax/(np.log(2.0))
        elif typ == 'median':
            opt_sigma = Dmedian/(np.log(2.0))
    elif kernel == 'gaussian':
        if typ == 'max':
            opt_sigma = Dmax/np.sqrt(2.0*(np.log(2.0)))
        elif typ == 'median':
            opt_sigma = Dmedian/np.sqrt(2.0*(np.log(2.0)))

    return opt_sigma



def prepare_trainingdata(descriptor,N_train,load_K,file_kernel,indices,lamd,X,Int_lam,sigmas,opt_sigma,cut_distance,max_size):


    N_bin=len(Int_lam[0])

    K=np.zeros([N_train,N_train],dtype=float)

    if descriptor == 'FCHL':
        if load_K:
            K = np.load(file_kernel)
        else:
            print('Calculating FCHL kernel elements'+'\n')
            for itrain in range(N_train):
                K[itrain,itrain]=1.0 + lamd
                if np.mod(itrain,10) == 0:
                    print(itrain, 'rows calculated', N_train-itrain, 'remaining')
                for jtrain in range(itrain+1,N_train):
                    Xt=X[indices[itrain]]
                    Xq=X[indices[jtrain]]
                    Yt=np.zeros([1,max_size,5,max_size],dtype=float)
                    Yq=np.zeros([1,max_size,5,max_size],dtype=float)
                    Yt[0]=Xt
                    Yq[0]=Xq
                    tmp=qml.fchl.get_global_kernels(Yq,Yt,sigmas=sigmas,cut_distance=cut_distance)
                    K[itrain,jtrain]=tmp[0,0,0]
                    K[jtrain,itrain]=K[itrain,jtrain]
            np.save(file_kernel, K)

    elif descriptor == 'SLATM':
        if load_K:
            K = np.load(file_kernel)
        else:
            print('Calculating SLATM kernel elements'+'\n')
            for itrain in range(N_train):
                K[itrain,itrain]=1.0 + lamd
                if np.mod(itrain,10) == 0:
                    print(itrain, 'rows calculated', N_train-itrain, 'remaining')
                for jtrain in range(itrain+1,N_train):
                    Xt=X[indices[itrain]]
                    Xq=X[indices[jtrain]]
                    Yt=np.zeros([1,len(Xt)],dtype=float)
                    Yq=np.zeros([1,len(Xq)],dtype=float)
                    Yt[0]=Xt
                    Yq[0]=Xq
                    tmp=laplacian_kernel(Yq,Yt, sigma=opt_sigma)
                    K[itrain,jtrain]=tmp[0,0]
                    K[jtrain,itrain]=K[itrain,jtrain]
            np.save(file_kernel, K)

    P=np.zeros([N_train,N_bin],dtype=float)

    for ibin in range(N_bin):
        for itrain in range(N_train):
            P[itrain,ibin]=Int_lam[indices[itrain],ibin]

    return K, P



def prepare_trainingdata_batch(N_train,file_kernel,indices,lamd,X,Int_lam,sigmas,cut_distance,max_size, s_batch, i_batch):


    N_bin=len(Int_lam[0])

    K=np.zeros([s_batch,N_train],dtype=float)

    print('Calculating FCHL kernel elements'+'\n')
    for itrain in range(s_batch*(i_batch-1), s_batch*(i_batch)):
        if np.mod(itrain,10) == 0:
            print(itrain, 'rows calculated', itrain, 'remaining')
        for jtrain in range(0,N_train):
            Xt=X[indices[itrain]]
            Xq=X[indices[jtrain]]
            Yt=np.zeros([1,max_size,5,max_size],dtype=float)
            Yq=np.zeros([1,max_size,5,max_size],dtype=float)
            Yt[0]=Xt
            Yq[0]=Xq
            tmp=qml.fchl.get_global_kernels(Yq,Yt,sigmas=sigmas,cut_distance=cut_distance)
            K[itrain-(s_batch*(i_batch-1)),jtrain]=tmp[0,0,0]
        K[itrain-(s_batch*(i_batch-1)), itrain]=1.0 + lamd
    np.savetxt(file_kernel, K)

    P=np.zeros([N_train,N_bin],dtype=float)

    for ibin in range(N_bin):
        for itrain in range(N_train):
            P[itrain,ibin]=Int_lam[indices[itrain],ibin]

    return K, P
