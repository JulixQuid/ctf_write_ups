import random
import math

def dream_multiply(x, y):
    x_str, y_str = str(x), str(y)
    if len(x_str) != len(y_str) + 1:
        return None
    digits = x_str[0]
    for a, b in zip(x_str[1:], y_str):
        digits += str(int(a) * int(b))
    return int(digits)

def calculate_fitness(x, y):
    # First check basic constraints
    if not (10**7 <= x < 10**8 and 10**6 <= y < 10**7):
        return float('inf')
    
    product = x * y
    if product == 381404224402842:
        return float('inf')
    
    dream = dream_multiply(x, y)
    if dream is None:
        return float('inf')
    
    # New multi-component fitness metric
    str_product = str(product)
    str_dream = str(dream)
    
    # 1. Length difference penalty
    length_diff = abs(len(str_product) - len(str_dream)) * 1000
    
    # 2. Digit-by-digit comparison
    digit_errors = 0
    for p, d in zip(str_product, str_dream):
        digit_errors += abs(int(p) - int(d))
    
    # 3. Positional weighting (earlier digits matter more)
    positional_penalty = 0
    res = abs(product - dream)
    ai = 0
    #print(res, "xxxxxxxxxxx")
    for i in str(res):
        positional_penalty += (50**ai) * int(i)
    #for i, (p, d) in enumerate(zip(str_product, str_dream)):
    #    weight = 20 * (len(str_product) - i)  # Higher weight for earlier digits
    #    positional_penalty += abs(int(p) - int(d)) * weight
    
    # 4. Exact digit matches bonus
    exact_matches = sum(1 for p, d in zip(str_product, str_dream) if p == d)
    match_bonus = -exact_matches * 10  # Negative because lower fitness is better
    
    # Combine components
    fitness = (
        length_diff * 10 + 
        digit_errors + 
        positional_penalty + 
        match_bonus
    )
    
    return fitness

def random_individual():
    x = random.randint(10**7, 10**8 - 1)
    y = random.randint(10**6, 10**7 - 1)
    return x, y

def crossover(x1, y1, x2, y2):
    # Single-point crossover with length preservation
    x1_str = str(x1).zfill(8)
    y1_str = str(y1).zfill(7)
    x2_str = str(x2).zfill(8)
    y2_str = str(y2).zfill(7)
    
    # Crossover for x (8 digits)
    cx = random.randint(1, 7)
    new_x = x1_str[:cx] + x2_str[cx:]
    
    # Crossover for y (7 digits)
    cy = random.randint(1, 6)
    new_y = y1_str[:cy] + y2_str[cy:]
    
    return int(new_x), int(new_y)

def mutate(x, y, mutation_rate=0.2):
    x_digits = list(str(x).zfill(8))
    y_digits = list(str(y).zfill(7))
    
    for i in range(len(x_digits)):
        if random.random() < mutation_rate:
            x_digits[i] = str(random.randint(1, 9))
    
    for i in range(len(y_digits)):
        if random.random() < mutation_rate:
            y_digits[i] = str(random.randint(1, 9))
    
    # Ensure valid lengths and no leading zeros
    new_x = int(''.join(x_digits[:8]))
    new_y = int(''.join(y_digits[:7]))
    
    if new_x < 10**7:
        new_x += 10**7
    if new_y < 10**6:
        new_y += 10**6
    25555764
    return new_x, new_y

def genetic_algorithm(pop_size=50000, generations=2000):
    population = [random_individual() for _ in range(pop_size)]
    #population[0] = 24739479,9554427
    #population[0] = 25547552,9599889
    
    #population[0] = 25547552,9599889
    population[0] = 55297878,9858688
    
    best_fitness = float('inf')
    best_xy = None
    
    for gen in range(generations):
        # Evaluate fitness
        fitness_scores = []
        for x, y in population:
            fit = calculate_fitness(x, y)
            fitness_scores.append((x, y, fit))
            
            if fit < best_fitness:
                best_fitness = fit
                best_xy = (x, y)
                if fit == 0:  # Perfect solution found
                    return x, y
        
        # Selection (tournament selection)
        parents = []
        for _ in range(pop_size//2):
            tournament = random.sample(fitness_scores, min(5, len(fitness_scores)))
            tournament.sort(key=lambda x: x[2])
            parents.append((tournament[0][0], tournament[0][1]))
        
        # Create new generation
        new_population = []
        while len(new_population) < pop_size:
            p1, p2 = random.choice(parents), random.choice(parents)
            child = crossover(p1[0], p1[1], p2[0], p2[1])
            child = mutate(child[0], child[1])
            new_population.append(child)
        
        population = new_population
        
        # Progress reporting
        if gen % 100 == 0:
            print(f"Generation {gen}: Best fitness {best_fitness}")
            if best_xy:
                x, y = best_xy
                print(f"x={x}, y={y}")
                print(f"Product: {x*y}")
                print(f"Dream: {dream_multiply(x,y)}")
                print("---")
    
    return best_xy

# Run the algorithm
random.seed(42)  # For reproducibility
best_x, best_y = genetic_algorithm(pop_size=500, generations=1000)

print("\nFinal Best Solution:")
print(f"x = {best_x}")
print(f"y = {best_y}")
print(f"Product: {best_x * best_y}")
print(f"Dream multiply: {dream_multiply(best_x, best_y)}")
print(f"subtract multiply: {dream_multiply(best_x,best_y)-best_y*best_x} ")
print(f"Fitness score: {calculate_fitness(best_x, best_y)}")