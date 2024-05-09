from cs50 import get_int

#get user input between 1 and 8
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

for i in range(height):
    num = i+1
    print((height-num) * " ", end="")
    print(num * "#", end="")
    print("")
    