#Primos Checker
prm= int(input("Inserte número primo: "))

fg= 1
for i in range(2,prm):
	if (prm% i) == 0:
		print(prm,"no es un numero primo :(")
		print("pq", prm//i, "multiplicado por",i,"es", prm)
		fg = 0
		break
if fg == 1:
	print(prm, "es un numero primo :o")
