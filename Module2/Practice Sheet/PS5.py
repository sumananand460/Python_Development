# String Methods

text = "  Hello Python World!  "

print(text.upper())           # HELLO PYTHON WORLD!
print(text.lower())           # hello python world!
print(text.strip())           # "Hello Python World!" (removes spaces)
print(text.replace("Python", "Java"))
print(text.split())           # ['Hello', 'Python', 'World!']
print("-".join(["a", "b", "c"]))  # "a-b-c"

print(text.startswith("Hello"))   # True
print(text.endswith("!"))         # True
print("123".isdigit())            # True
print("abc".isalpha())            # True
print("abc123".isalnum())         # True