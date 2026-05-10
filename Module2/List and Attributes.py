"""
What is a list?

=> A list is a mutable sequence of individual items, separated by commas and enclosed within 
a square bracket.

Attributes: 
* append(element)
* insert
* extend
"""

a = [1,3.98, "Suman"]
a.append("BATMAN")
a.insert(3, "Bruce")
a.extend(["dog", "cat", 2034.343])

print(a)