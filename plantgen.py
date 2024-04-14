import random

# Define the L-system rules
rules = {
    'F': ['FF+[+F-F-F]-[-F+F+F]', 'F[+F]F[-F]F', 'FF-[-F+F+F]+[+F-F-F]']
}

def generate_plant(axiom, rules, iterations):
    # Start with the axiom
    l_system_string = axiom
    # Iterate the L-system
    for _ in range(iterations):
        new_l_system_string = ''
        for character in l_system_string:
            if character in rules:
                new_l_system_string += random.choice(rules[character])
            else:
                new_l_system_string += character

        l_system_string = new_l_system_string

    return l_system_string

def generate_garden(size, iterations):
    garden = []
    for _ in range(size):
        garden.append(generate_plant('F', rules, iterations))
    
    return garden

# Main function
def main():
    # Parameters
    seed = 'F'
    iterations = 2

    # Generate the L-system string
    l_system_string = generate_plant(seed, rules, iterations)

    print(l_system_string)

if __name__ == "__main__":
    main()

