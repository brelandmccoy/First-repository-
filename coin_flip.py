import random

def coin_flip():
    return random.choice(['Heads', 'Tails'])

# Generate results
results = [coin_flip() for i in range(15)]

print("coin flip results:", results)