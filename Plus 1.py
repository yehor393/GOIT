n = int(input("Enter range of number: "))

sum = 0

for _ in range(1, n + 1):
    num = int(input("Enter value: "))
    sum += num

print(f"Sum equal {sum} and average value equal {round(sum/n,2)}")