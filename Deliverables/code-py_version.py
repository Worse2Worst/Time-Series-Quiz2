
# coding: utf-8

# In[30]:


import random
import math
import matplotlib.pyplot as plt
import pylab
import pandas as pd
import numpy as np
import statistics
import scipy.stats as st


# # 1. and 2.
# # Initilize values 

# In[67]:


X = 6
Y = 5
Z = 4
n = 2**X
w = 2**Y


# # 3. Create time series files of length n

# In[72]:


# results = []
# for _ in range(n):
#     random_number = "{0:.2f}".format(random.uniform(0, X))
#     results.append(random_number)
# outfile = open('test.txt', 'w+')
# outfile.write("\n".join(results))
# outfile.close()


# # Load both time series

# In[73]:


with open('time_series_data1.txt') as f:
    ts1 = f.read().splitlines()
ts1 = [float(x) for x in ts1]

with open('time_series_data2.txt') as f:
    ts2 = f.read().splitlines()
ts2 = [float(x) for x in ts2]


# # (optional) Plot the original time series data

# In[74]:


plt.plot(ts1,'r',label = 'ts1')
plt.plot(ts2,'b',label = 'ts2')
pylab.legend()
plt.show()


# # 4. Z-normalize both Time series

# In[75]:


def z_normalize(ts):
    z_mean = statistics.mean(ts)
    z_sd = statistics.pstdev(ts)
    return [(x-z_mean)/z_sd for x in ts]


# In[76]:


z1 = z_normalize(ts1)
z2 = z_normalize(ts2)
z1 = [float("{0:.2f}".format(x)) for x in z1] # roundind the z1
z2 = [float("{0:.2f}".format(x)) for x in z2] # roundind the z2


# # Save the normalized data to files

# In[77]:


z1_string = [str(x) for x in z1] # convert to string to write
z2_string = [str(x) for x in z2] # convert to string to write
# First file
outfile = open('normailzed_ts1.txt', 'w+')
outfile.write("\n".join(z1_string))
outfile.close()

# Second file
outfile = open('normailzed_ts2.txt', 'w+')
outfile.write("\n".join(z2_string))
outfile.close()


# # (optional) Plot the normalized data

# In[78]:


plt.plot(z1,'r',label = 'z1')
plt.plot(z2,'b',label = 'z2')
pylab.legend()
plt.show()


# # 5. convert both Time Series into SAX string
# # First, convert to PAA

# In[79]:


def PAA(ts, M):
    n = len(ts)
    chunk_size = float(n) / M
    step = int(math.ceil(chunk_size))
    res = [0]*M
    loop = 0
    ptr = int(loop * chunk_size)
    for i in range(n*M):
        idx = int(i/n)
        pos = int(i/M)
        res[idx] = res[idx] + ts[pos]
         
    for i in range(M):
        res[i] = res[i] / n
    return res


# In[80]:


paa1 = PAA(z1,2**Y)
paa2 = PAA(z2,2**Y)
paa1 = [float("{0:.2f}".format(x)) for x in paa1] # roundind the PAA1
paa2 = [float("{0:.2f}".format(x)) for x in paa2] # roundind the PAA2


# # Create breakpoints

# In[81]:


breakpoints = [0]*(Z-1)
for i in range(len(breakpoints)):
    area_size = (i+1)/Z
    breakpoints[i] = st.norm.ppf(area_size)


# # Mapping, PAA -> Alphabets

# In[82]:


def map_to_alphabets(num,breakpoints,alphabets):
    for i in range(len(breakpoints)):
        if num < breakpoints[i]:
            return alphabets[i]
    return alphabets[i+1]        


# In[83]:


alphabets = ('a','b','c','d')
SAX_A = []
SAX_B = [] 
for num in paa1 :
    SAX_A.append(map_to_alphabets(num,breakpoints,alphabets))
for num in paa2 :
    SAX_B.append(map_to_alphabets(num,breakpoints,alphabets))


# In[84]:


''.join(SAX_A)


# In[85]:


''.join(SAX_B)


# # 6. Calculate a distance between SAX_A and SAX_B

# # Create a lookup table for the distances

# In[86]:


distances_table = np.zeros(shape=(Z,Z))
for r in range(Z):
    for c in range (Z):
        if (abs(r-c) > 1):
            distances_table[r][c] = breakpoints[max(r,c)-1] - breakpoints[min(r,c)]


# In[87]:


def character_distance(c1,c2,table):
    return table[ord(c1)-ord('a')][ord(c2)-ord('a')]


# In[88]:


dist = 0
for i in range(len(SAX_A)):
    c1 = SAX_A[i]
    c2 = SAX_B[i]
    dist+=  character_distance(c1,c2,distances_table)


# In[89]:


# The distance between SAX_A and SAX_B, rounding to 2 decimal points.
float("{0:.2f}".format(dist))

