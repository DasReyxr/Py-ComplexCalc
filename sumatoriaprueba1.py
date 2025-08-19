max = (int(input("Introduce numero maximo: ")))

# initialize sum and counter
sum = 0
ini = (int(input("Introduce numero inicial: ")))

while ini <= max:
    sum = sum+ini
    ini+=1    # update counter

print("The sum is", sum)