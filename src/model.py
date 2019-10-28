import numpy as np
#import OpenTextbot.src.Algebra as Algebra
from sklearn.cluster import KMeans
#from sklearn.cluster import MiniBatchKMeans

def GetCentroidArrayWE(ArrayWE, index2D):
  CentroidArrayWE = []
  for i in range(len(index2D)):
    CurrentArrayWE = []
    for j in range(len(index2D[i])):
      CurrentArrayWE.append(ArrayWE[index2D[i][j]])
    kmeans = KMeans(n_clusters=1, random_state=0).fit(CurrentArrayWE)
    CentroidWE = kmeans.cluster_centers_
    CentroidArrayWE.append(CentroidWE[0])
  return CentroidArrayWE
