y1 = 5  
x1 = 6  
y2 = 3.5
x2 = -9

print("The first coordinate is", (x1, y1))
print("The second coordinate is", (x2, y2))

# calculate the result
slope = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')

# fancy print the output with two decimal places for floating number
print(f"The slope of the line is {slope:.2f}")
