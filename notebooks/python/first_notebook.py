
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#problem" data-toc-modified-id="problem-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>problem</a></span></li><li><span><a href="#Python-solution-1:-simple-script" data-toc-modified-id="Python-solution-1:-simple-script-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Python solution 1: simple script</a></span></li><li><span><a href="#Python-solution-2:-function-with-for-loop" data-toc-modified-id="Python-solution-2:-function-with-for-loop-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Python solution 2: function with for loop</a></span></li><li><span><a href="#Python-solution-3:-using-a-numpy-array" data-toc-modified-id="Python-solution-3:-using-a-numpy-array-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Python solution 3: using a numpy array</a></span></li></ul></div>

# # problem
# 
# -  Read [Stull Chapter 2 pages 27-29](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch02-radiation-v102b.pdf) and write a program that computes the true anomaly $\nu$ using (2.3b) for given a date of April 12 (day 102).  

# <img src="screenshots/stull_eq_2_3.png">

# # Python solution 1: simple script
# 
# * import functions from the numpy module following [the Whirlwind module section](https://github.com/jakevdp/WhirlwindTourOfPython/blob/master/14-Strings-and-Regular-Expressions.ipynb)
# 
# * print out a formatted string following [the Whirlwind "Format strings" section](http://clouds.eos.ubc.ca/~phil/courses/atsc301/whirlwind/14-Strings-and-Regular-Expressions.html)
# 
# 

# In[17]:


from numpy import sin, pi

d=102
C=2*pi
P= 365.256363 #sidereal orbital period (Stull p. 29)
dp = 4 #day of perihelion
M = C*(d - dp)/P  #Stull eq. 2.2
nu = M + 0.0333988*sin(M) +  0.0003486*sin(2*M) + 0.0000050*sin(3*M)  #Stull eq. 2.3b
print("For day 102:\nDay number = {}, M={:5.3f} rads, nu = {:5.3f} rads".format(d, M, nu))


# # Python solution 2: function with for loop
# 
# Write a function in a loop following the [Whirlwind Functions section](http://clouds.eos.ubc.ca/~phil/courses/atsc301/whirlwind/08-Defining-Functions.html)

# In[18]:


def find_nu(day_num):
    """
    find the true anomoly nu using stull equation 2.3b
    
    Parameters
    ----------
    
    day_num: float or array
        number of day in year
        
    Returns
    -------
    
    M, nu : float or array
       M (radians) is the mean anomaly
       nu (radians) is the true anomaly
    """
    C=2*pi
    P= 365.256363 #sidereal orbital period (Stull p. 29)
    dp = 4 #day of perihelion
    M = C*(day_num - dp)/P  #Stull eq. 2.2
    nu = M + 0.0333988*sin(M) +  0.0003486*sin(2*M) + 0.0000050*sin(3*M)  #Stull eq. 2.3b
    return M,nu

days = [4,18,32,46,60,74,88,102,116,172,266,356]  #put the days in alist
#iterate over each value in the list
for day_num in days:
    M,nu = find_nu(day_num)
    print("Day number = {}, M={:5.3f} rads, nu = {:5.3f} rads".format(day_num, M, nu))
    


# # Python solution 3: using a numpy array
# 
# Like Matlab or R, python can do vector and matrix operations that run much faster than for loops
# 
# See [Pine section 3.3](http://clouds.eos.ubc.ca/~phil/djpine_python/chap3/chap3_arrays.html#numpy-arrays) for the array syntax or the [handbook numpy notebook](https://github.com/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/02.02-The-Basics-Of-NumPy-Arrays.ipynb)

# In[19]:


days_array = np.array(days)
days_array


# In[20]:


M, nu = find_nu(days_array)
print(type(M),type(nu))


# In[21]:


M


# In[22]:


nu


# See [the Whirlwind iterators section](http://clouds.eos.ubc.ca/~phil/courses/atsc301/whirlwind/10-Iterators.html) for an introduction to the zip function used below.  How would you do the following in Matlab?

# In[23]:


for the_day, the_M, the_nu in zip(days_array,M,nu):
    print("Day number = {}, M={:5.3f} rads, nu = {:5.3f} rads".format(the_day, the_M, the_nu))

