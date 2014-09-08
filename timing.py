import time

magic_num = 100000000
t1 = time.time()
array1 = []
for i in xrange(0,magic_num):
	array1.append(i**2)
print(time.time()-t1)