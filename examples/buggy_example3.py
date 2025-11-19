# Example 3: Type error - concatenating string and integer
def greet_user(name, age):
    message = "Hello, " + name + "! You are " + age + " years old."
    return message

user_name = "Alice"
user_age = 25
greeting = greet_user(user_name, user_age)
print(greeting)
