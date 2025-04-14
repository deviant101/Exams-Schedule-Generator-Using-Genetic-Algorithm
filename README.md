# Exam Schedule Generator Using Genetic Algorithm

## 📝 Overview

This document provides a comprehensive explanation of an **Exam Schedule Generator** system implemented using a **Genetic Algorithm** approach. The system creates optimal exam schedules by considering multiple constraints, balancing requirements, and evolving solutions over generations to find the best possible exam timetable.

## 🎯 Problem Statement

Creating an exam schedule involves complex constraints:

- No student should have overlapping exams
- No teacher should be assigned to multiple exams at the same time
- Exams should be scheduled only on weekdays
- Exams should be held during reasonable hours (9 AM - 5 PM)
- Teachers should not have consecutive invigilation duties
- Various soft constraints for student and faculty convenience

This is a classic NP-hard problem that can be effectively approached with metaheuristic techniques like genetic algorithms.

## 🧬 Genetic Algorithm Approach

The system uses a genetic algorithm with the following components:

1. **Chromosome Representation**: Each chromosome represents a complete exam schedule
2. **Fitness Function**: Evaluates how well a schedule satisfies constraints
3. **Selection**: Uses roulette wheel selection to choose parent schedules
4. **Crossover**: Implements two-point crossover to generate children schedules
5. **Mutation**: Introduces random changes to maintain genetic diversity
6. **Evolution**: Repeats the process over multiple generations

## 💻 Implementation Details

### Chromosome Class

The `Chromosome` class represents an individual exam schedule with:

```python
class Chromosome:
    def __init__(self, schedule):
        """Initialize a Chromosome with a given schedule.
        Calculate the fitness and constraints fulfilled for the schedule."""
        self.schedule = schedule
        self.fitness, self.constraints_fulfilled = self.calculate_fitness()

    def calculate_fitness(self):
        """
        Calculate the fitness of the schedule.
        Check various constraints and calculate penalties and rewards.
        
        Returns:
        tuple: Fitness value and list of constraints fulfilled.
        """
        # Implementation details for fitness calculation
```

The fitness function calculates a score based on:
- Penalties for violated hard constraints
- Rewards for fulfilled soft constraints

### Key Functions

#### Initial Population Generation

```python
def initialize_population(size):
    """
    Generate initial population of random schedules.
    
    Args:
        size (int): Number of chromosomes in population
        
    Returns:
        list: List of Chromosome objects representing initial population
    """
    # Implementation to create random schedules
```

#### Genetic Operators

1. **Selection**:
```python
def roulette_wheel_selection(population):
    """Select a chromosome using roulette wheel selection."""
    # Implementation of selection mechanism
```

2. **Crossover**:
```python
def crossover(parent1, parent2):
    """Perform intelligent crossover between two parent schedules."""
    # Implementation of two-point crossover with conflict resolution
```

3. **Mutation**:
```python
def mutate(chromosome, mutation_rate):
    """Perform intelligent mutation on a chromosome's schedule."""
    # Implementation of mutation with conflict resolution
```

4. **Main Genetic Algorithm**:
```python
def genetic_algorithm(population_size, generations, mutation_rate):
    """Execute the genetic algorithm with detailed progress tracking."""
    # Implementation of the main evolutionary loop
```

### Constraints Handling

The system checks for multiple types of constraints:

1. **Hard Constraints**:
   - No overlapping exams for students
   - No overlapping exams for teachers
   - Exams scheduled only on weekdays
   - Exams scheduled between 9 AM and 5 PM
   - No consecutive invigilation duties for teachers

2. **Soft Constraints**:
   - Common break on Friday from 1-2 PM
   - No back-to-back exams for students
   - MG courses scheduled before CS courses
   - Two-hour break for faculty meetings

### Result Presentation

The system presents the optimal solution with:
- A formatted schedule table
- Fitness score information
- List of fulfilled constraints
- Evolution progress statistics

## 🚀 Usage

```python
# Configure parameters
population_size = 50
generations = 50
mutation_rate = 0.05

# Run the genetic algorithm
best_solution, stats = genetic_algorithm(population_size, generations, mutation_rate)

# Display results
display_final_results(best_solution, stats)
```

## 📊 Results Analysis

The genetic algorithm typically shows rapid improvement in early generations followed by more gradual optimization:

- Initial generations: Fitness scores around -14 to -20
- Middle generations: Fitness improves to around -5 to -3
- Final generations: Stabilizes around -1 (near-optimal solution)

The final solution satisfies most constraints, with typically over 425 constraints fulfilled out of the total.

## 📈 Performance Optimization

The system employs several optimization techniques:

1. **Intelligent Crossover**: Resolves teacher conflicts during crossover operations
2. **Adaptive Mutation**: Selectively mutates different aspects (day, time, room, teacher)
3. **Conflict Resolution**: Actively finds alternative teachers for conflicting assignments
4. **Early Convergence Handling**: Maintains genetic diversity through controlled mutation

## 🔍 Limitations and Future Work

While the system produces high-quality exam schedules, potential improvements include:

1. **Parallel Computing**: Implementing parallel fitness evaluation for larger problems
2. **Hybrid Approaches**: Combining genetic algorithms with local search techniques
3. **Dynamic Constraints**: Supporting runtime adjustable constraints
4. **Multi-Objective Optimization**: Handling multiple competing objectives explicitly
5. **Interactive Refinement**: Allowing manual adjustments to algorithmically generated schedules

## 🗃️ Data Structures

The main data structures used:

1. **Schedule**: Dictionary mapping courses to tuples of (day, time, room, teacher)
2. **Population**: List of Chromosome objects
3. **Constraints**: Lists of string descriptions of fulfilled constraints
4. **Generation Statistics**: Tracking of fitness and constraints over algorithm execution

## 🧮 Algorithm Complexity

- **Time Complexity**: O(G * P * C²), where G is generations, P is population size, and C is number of courses
- **Space Complexity**: O(P * C), where P is population size and C is number of courses

## 🏆 Conclusion

The genetic algorithm approach to exam scheduling demonstrates the power of evolutionary computation in solving complex combinatorial problems. By defining appropriate chromosome representations, fitness functions, and genetic operators, the system successfully generates high-quality exam schedules that satisfy the majority of constraints.