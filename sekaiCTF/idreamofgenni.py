import random


def dream_multiply(x, y):
    x_str, y_str = str(x), str(y)
    if len(x_str) != len(y_str) + 1:
        return float('inf')
    digits = x_str[0]
    for a, b in zip(x_str[1:], y_str):
        digits += str(int(a) * int(b))
    return int(digits)

def fitness(x, y):
    product = x * y
    if product == 381404224402842:
        return float('inf')
    dream = dream_multiply(x, y)
    if dream == float('inf'):
        return float('inf')
    return abs(product - dream)

def random_individual():
    x = random.randint(10**7, 10**8 - 1)
    y = random.randint(10**6, 10**7 - 1)
    return x, y

def crossover(x1, y1, x2, y2):
    x1_str = str(x1).zfill(8)
    y1_str = str(y1).zfill(7)
    x2_str = str(x2).zfill(8)
    y2_str = str(y2).zfill(7)
    
    cx = random.randint(1, 7)
    new_x = x1_str[:cx] + x2_str[cx:]
    
    cy = random.randint(1, 6)
    new_y = y1_str[:cy] + y2_str[cy:]
    
    if new_y[0] == '0':
        new_y = '9' + new_y[1:]
    if new_x[0] == '0':
        new_x = '1' + new_x[1:]
    
    return int(new_x), int(new_y)

def mutate(x, y, mutation_rate=0.5):
    x_digits = list(str(x).zfill(8))
    y_digits = list(str(y).zfill(7))
    
    for i in range(8):
        if random.random() < mutation_rate:
            x_digits[i] = str(random.randint(1, 9))
            if i == 0 and x_digits[0] == '0':
                x_digits[0] = str(random.randint(1, 9))
    
    for i in range(7):
        if random.random() < mutation_rate:
            y_digits[i] = str(random.randint(1, 9))
            if i == 0 and y_digits[0] == '0':
                x_digits[0] = str(random.randint(1, 9))
    
    return int(''.join(x_digits)), int(''.join(y_digits))

def genetic_algorithm(pop_size=10000, generations=2000):
    population = [random_individual() for _ in range(pop_size)]
    #population[0] = 15378656 , 9436595
    population[0] = 18549592 , 8862859
    best_fitness = float('inf')
    
    for gen in range(generations):
        fitness_scores = []
        for x, y in population:
            fit = fitness(x, y)
            fitness_scores.append((x, y, fit))
        
        fitness_scores.sort(key=lambda x: x[2])
        current_best = fitness_scores[0][2]
        
        if current_best < best_fitness:
            best_fitness = current_best
            best_x, best_y = fitness_scores[0][0], fitness_scores[0][1]
        
        if gen % 100 == 0:
            print(f"Gen {gen}: Best difference {best_x} {best_y} {x*y} {current_best}")
        
        if current_best == 0:
            return fitness_scores[0][0], fitness_scores[0][1]
        
        parents = [(x, y) for x, y, _ in fitness_scores[:pop_size//2]]
        
        new_population = parents.copy()
        while len(new_population) < pop_size:
            p1, p2 = random.choice(parents), random.choice(parents)
            child = crossover(p1[0], p1[1], p2[0], p2[1])
            child = mutate(child[0], child[1])
            new_population.append(child)
        
        population = new_population
    
    return best_x, best_y

x, y = genetic_algorithm()
print(f"\nBest solution found:")
print(f"x = {x} (8-digit)")
print(f"y = {y} (7-digit)")
print(f"x * y = {x * y}")
print(f"dream_multiply(x, y) = {dream_multiply(x, y)}")
print(f"Difference: {abs(x * y - dream_multiply(x, y))}")