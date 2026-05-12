# Loops:

''''
for i in range (10,0,-1):
    print(i)
print("Blast off!")
'''

'''
# Printing a table using for loop:
num = int(input("Enter your number: "))

for i in range(1,11):
    print(f"{num} x {i} = {num * i}")
'''

total = 0

while True:                              # Infinite loop
    num = int(input("Enter a number (0 to stop): "))
    if num == 0:
        break                            # Exit loop when 0 is entered
    total += num                         # Same as total = total + num

print(f"Total sum: {total}")