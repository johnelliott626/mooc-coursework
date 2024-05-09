from cs50 import get_float

# get valid input
amount = -1
while amount < 0:
    amount = get_float("Change owed: ") * 100

# initialize the number of coins to 0, and iterate over each coin,
# calculating the number of coins needed to give change
coins = 0
for i in [25, 10, 5, 1]:
    if amount/i >= 1:
        coins += int(amount/i)
        amount -= (i * int(amount/i))

# print output
print(coins)
    