import numpy as np

dim=101
a=np.array(range(1,dim))

d=7
l=10
n=(dim-l)/d

if l%d == 0 :
	n+=1

b=np.zeros(shape=(n, l),dtype=np.int32)

print b.shape

for i in range(n): 
	ii=i*d

	print i, ii

	b[i,:]=a[ii:l+ii] 
	
print b
