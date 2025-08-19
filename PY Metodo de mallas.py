#PY metodo de mallas
aa= float(input("Inserte aa: "))
ba= float(input("Inserte ba: "))
ca= float(input("Inserte ca: "))
ab= float(input("Inserte ab: "))
bb= float(input("Inserte bb: "))
cb= float(input("Inserte cb: "))
ac= float(input("Inserte ac: "))
bc= float(input("Inserte bc: "))
cc= float(input("Inserte cc: "))
print("\n")
v1= float(input("Inserte v1: "))
v2= float(input("Inserte v2: "))
v3= float(input("Inserte v3: "))
print("\n")

print([aa,ba,ca])
print([ab,bb,cb])
print([ac,bc,cc])

D_1=(aa*bb*cc)+(ab*bc*ca)+(ac*ba*cb)
D_2=(bb*ac*ca)+(aa*bc*cb)+(cc*ab*ba)
Delta=D_1-D_2
print(D_1,"-",D_2,"es:" ,Delta)
print("\n")
#IA
print("IA")
print([v1,ba,ca])
print([v2,bb,cb])
print([v3,bc,cc])

Da_1=(v1*bb*cc)+(v2*bc*ca)+(v3*ba*cb)
Da_2=(bb*v3*ca)+(v1*bc*cb)+(cc*v2*ba)
Da=Da_1-Da_2
print("Delta A es= ",Da)
Ia=Da/Delta
print(Ia)
print("\n")
#IB
print("IB")
print([aa,v1,ca])
print([ab,v2,cb])
print([ac,v3,cc])

Db_1=(aa*v2*cc)+(ab*v3*ca)+(ac*v1*cb)
Db_2=(v2*ac*ca)+(aa*v3*cb)+(cc*ab*v1)
Db=Db_1-Db_2
print("Delta B es= ",Db)
Ib=Db/Delta
print(Ib)
print("\n")

#IC

print("IC")
print([aa,ba,v1])
print([ab,bb,v2])
print([ac,bc,v3])

Dc_1=(aa*bb*v3)+(ab*bc*v1)+(ac*ba*v2)
Dc_2=(bb*ac*v1)+(aa*bc*v2)+(v3*ab*ba)
Dc=Dc_1-Dc_2
print("Delta C es= ",Dc)
Ic=Dc/Delta
print(Ic)
print("\n")