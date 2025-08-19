import numpy as np 
#Array
ones  = np.ones((3,4))
zeros = np.zeros((3,4))
full  = np.full((2,2),9)
ide1  = np.eye(4,4)
ide2  = np.identity(4)
print(f"Ones \n{ones}\n")
print(f"Zeros \n{zeros}\n")
print(f"Nines \n{full}\n")
print(f"Id1 \n{ide1}\n")
print(f"Id2 \n{ide2}\n")


E1= np.arange(0,30,5) #Start,Limit, Up
E2= np.linspace(0,2,6) #Start Limit, in x spaces divide all numbers
print(f"Arange {E1}\n") 
print(f"Linspace {E2}\n")
#Dimensions 
d0= np.array(23)
print(f"Array d0: {d0}")
print(f"Dimension {d0.ndim}")

d1= np.array([1,2,3,4])
print(f"Array d1: {d1}")
print(f"Dimension {d1.ndim}")

d2= np.array([[1,2,3,4],[9,8,7,6]])
print(f"Array d2: \n{d2}")
print(f"Dimension {d2.ndim}")
d2=d2.reshape(4,2)

print(f"NEW Array d2: \n{d2}")
print(f"Dimension {d2.ndim}")
d3= np.array([[[1,2,3],[9,8,7]],[[2,4,5],[3,5,9]]])
print(f"Array d3: \n{d3}")
print(f"Dimension {d3.ndim}")

#ndimensions
dn= np.array([2,3,4],ndmin=5)
print(dn)
print(f"N-Dimension {dn.ndim}")


a1= np.array([1,2,3])
t1= np.array((1,2,3))
print(f"Array is: {a1}")
print(f"Type {type(a1)}")

print(f"Tuple is: {t1}")
print(f"Type {type(t1)}")

