import math

"""
Use the Gauss-Legendre Algorithm to estimate Pi. Perform 10 approximation loops. Once complete, return the approximation.
:return:
"""

# a variable to hold your returned estimate for PI. When you are done,
# set your estimated value to this variable. Do not change this variable name
pi_estimate = 3.141592653589794

"""
Step 1: Declare and initialize all the values for the Gauss-Legendre algorithm
"""

# modify these lines to correct set the variable values
a0 = 1
b0 = 1 / math.sqrt(2)
p0 = 1
t0 = 1 / 4

# perform 10 iterations of this loop
for i in range(1, 10):
    """
    Step 2: Update each variable based upon the algorithm. Take care to ensure
    the order of operations and dependencies among calculations is respected. You
    may wish to create new "temporary" variables to hold intermediate results
    """

    ### YOUR CODE HERE ###
    a = (a0 + b0) / 2
    b = math.sqrt(a0 * b0)
    p = 2 * p0
    t = t0 - p0 * (a0 - a) ** 2

    a0 = a
    b0 = b
    p0 = p
    t0 = t
    

    # print out the current loop iteration. This is present to have something in the loop.
    print("Loop Iteration: ", i)

"""
Step 3: After iterating 10 times, calculate the final value for PI
"""

# modify this line below to estimate PI
pi_estimate = (a0 + b0) ** 2 / (4 * t0)

print("Final estimate for PI: ", pi_estimate)
print("Error on estimate: ", abs(pi_estimate - math.pi))
