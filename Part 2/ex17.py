import random
name = input("Enter your name: ")
adjectives = ["Sneaky", "Mysterious", "Silent", "Gay", "Stupid", "Stubborn"]
animals = ["Gorilla", "Monkey", "Panda", "Pig", "Tiger", "Rabbit"]
adjective = random.choice(adjectives)
animal = random.choice(animals)
codename = adjective + " " + animal
lucky_number = random.randint(1,99)
print(f"{name}, your codename is: {codename}")
print(f"Your lucky number is: {lucky_number}")
