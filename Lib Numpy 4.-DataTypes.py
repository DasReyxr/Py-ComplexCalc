from unicodedata import name
import numpy as np 

# i - integer
# b - boolean
# u - unsigned integer
# f - float
# c - complex float
# m - timedelta
# M - datetime
# O - object
# S - string
# U - unicode string
# V - fixed chunk of memory for other type ( void )

#Dimensions 
flt_arr= np.array([1.1,2.2,3.3,4.4,5.1,6.2,7.3,8.0])
str_arr= np.array(["Juan","Pepe","Francisco"])
str_int_arr = np.array([1,2,3,4,5,6,7,8],dtype='U')
char_arr= np.array(["a","b","c"],dtype='S')
#With numbers we can set the size with u(unsigned), i(integer),f(float)
def name_type(array):
    print(f"Array d0: {array}")
    print(f"Type: {array.dtype}\n")


name_type(flt_arr)
name_type(str_arr)
name_type(str_int_arr)
name_type(char_arr)

#float->int
int_arr = flt_arr.astype("i")
name_type(int_arr)
#int->bool
int_arr2 = np.array([1,2,0,3,4,0,5,0,8])
bool_arr = int_arr2.astype(bool)
name_type(bool_arr)