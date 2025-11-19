# Example 2: Runtime error - division by zero
def divide_numbers(a, b):
    return a / b

numbers = [10, 20, 30, 0, 40]
for num in numbers:
    result = divide_numbers(100, num)
    print(f"100 / {num} = {result}")
