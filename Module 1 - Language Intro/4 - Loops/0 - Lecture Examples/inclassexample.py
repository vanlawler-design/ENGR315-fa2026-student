
import random

def generate_random_int_list(max_length, upper_bound):
    list_length = int(random.uniform(2, max_length))

    # given the length above, sample the Natural Numbers up to upper_bound that many times
    vars = random.sample(range(upper_bound), list_length)

    # return the generated list
    return vars

temperatures = generate_random_int_list(10, 100)


for temperature in temperatures:
    print(f"Current temperature: {temperature}°F")
    if temperature > 80:
        print("Warning: High temperature detected!")
    else:
        print("Temperature is normal.")