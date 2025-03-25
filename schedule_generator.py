import pandas as pd
import numpy as np
import random
from tabulate import tabulate

# Load datasets
teachers = pd.read_csv('Dataset/teachers.csv')
students = pd.read_csv('Dataset/studentNames.csv')
student_courses = pd.read_csv('Dataset/studentCourse.csv')
courses = pd.read_csv('Dataset/courses.csv')

# Define constants
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIMESLOTS = ['9-11', '11-1', '2-4', '4-6']
CLASSROOMS = [f'C{i}' for i in range(301, 311)]

# Define the chromosome structure
class Chromosome:
    def __init__(self, schedule):
        self.schedule = schedule
        self.fitness, self.constraints_fulfilled = self.calculate_fitness()

    def calculate_fitness(self):
        fitness = 0
        penalties = 0
        rewards = 0
        constraints_fulfilled = []

        # Essential Requirements
        # Check for overlapping exams for students
        for student in students['Names']:
            student_courses_list = student_courses[student_courses['Student Name'] == student]['Course Code'].tolist()
            exam_times = [(self.schedule[course][0], self.schedule[course][1]) for course in student_courses_list]
            if len(exam_times) != len(set(exam_times)):
                penalties += 1
            else:
                constraints_fulfilled.append(f"No overlapping exams for student {student}")

        # Check for overlapping exams for teachers
        for teacher in teachers['Names']:
            teacher_exams = [course for course, details in self.schedule.items() if details[3] == teacher]
            exam_times = [(self.schedule[course][0], self.schedule[course][1]) for course in teacher_exams]
            if len(exam_times) != len(set(exam_times)):
                penalties += 1
            else:
                constraints_fulfilled.append(f"No overlapping exams for teacher {teacher}")

        # Check for exams scheduled only on weekdays
        for course, details in self.schedule.items():
            if details[0] not in DAYS:
                penalties += 1
            else:
                constraints_fulfilled.append(f"Exam for course {course} scheduled on a weekday")

        # Check for exam timings between 9 AM and 5 PM
        for course, details in self.schedule.items():
            if details[1] not in TIMESLOTS:
                penalties += 1
            else:
                constraints_fulfilled.append(f"Exam for course {course} scheduled between 9 AM and 5 PM")

        # Check for consecutive exam invigilation duties for teachers
        for teacher in teachers['Names']:
            teacher_exams = [course for course, details in self.schedule.items() if details[3] == teacher]
            teacher_exams.sort(key=lambda x: (self.schedule[x][0], self.schedule[x][1]))
            for i in range(len(teacher_exams) - 1):
                if self.schedule[teacher_exams[i]][0] == self.schedule[teacher_exams[i + 1]][0]:
                    penalties += 1
                else:
                    constraints_fulfilled.append(f"No consecutive invigilation duties for teacher {teacher}")

        # Optimization Criteria
        # Common break on Friday from 1-2 PM
        friday_exams = [details for course, details in self.schedule.items() if details[0] == 'Friday']
        if all(details[1] != '1-2' for details in friday_exams):
            rewards += 1
            constraints_fulfilled.append("Common break on Friday from 1-2 PM")

        # No back-to-back exams for students
        for student in students['Names']:
            student_courses_list = student_courses[student_courses['Student Name'] == student]['Course Code'].tolist()
            exam_times = [(self.schedule[course][0], self.schedule[course][1]) for course in student_courses_list]
            exam_times.sort()
            for i in range(len(exam_times) - 1):
                if exam_times[i][0] == exam_times[i + 1][0] and abs(TIMESLOTS.index(exam_times[i][1]) - TIMESLOTS.index(exam_times[i + 1][1])) == 1:
                    penalties += 1
                else:
                    constraints_fulfilled.append(f"No back-to-back exams for student {student}")

        # MG course before CS course
        for student in students['Names']:
            student_courses_list = student_courses[student_courses['Student Name'] == student]['Course Code'].tolist()
            mg_courses = [course for course in student_courses_list if course.startswith('MG')]
            cs_courses = [course for course in student_courses_list if course.startswith('CS')]
            for mg_course in mg_courses:
                for cs_course in cs_courses:
                    if (self.schedule[mg_course][0], self.schedule[mg_course][1]) > (self.schedule[cs_course][0], self.schedule[cs_course][1]):
                        penalties += 1
                    else:
                        constraints_fulfilled.append(f"MG course {mg_course} scheduled before CS course {cs_course}")

        # Two-hour break for faculty meetings
        faculty_free_slots = {slot: 0 for slot in TIMESLOTS}
        for course, details in self.schedule.items():
            faculty_free_slots[details[1]] += 1
        if any(count <= len(teachers) / 2 for count in faculty_free_slots.values()):
            rewards += 1
            constraints_fulfilled.append("Two-hour break for faculty meetings")

        fitness = rewards - penalties
        return fitness, constraints_fulfilled

# Initialize population
def initialize_population(size):
    population = []
    for _ in range(size):
        schedule = generate_random_schedule()
        population.append(Chromosome(schedule))
    return population

def generate_random_schedule():
    schedule = {}
    for index, course in courses.iterrows():
        day = random.choice(DAYS)
        timeslot = random.choice(TIMESLOTS)
        classroom = random.choice(CLASSROOMS)
        teacher = random.choice(teachers['Names'])
        schedule[course['Course Code']] = (day, timeslot, classroom, teacher)
    return schedule

# Selection using roulette wheel
def roulette_wheel_selection(population):
    max_fitness = sum([chromosome.fitness for chromosome in population])
    if max_fitness == 0:
        return random.choice(population)
    pick = random.uniform(0, max_fitness)
    current = 0
    for chromosome in population:
        current += chromosome.fitness
        if current > pick:
            return chromosome
    return random.choice(population)

# Crossover
def crossover(parent1, parent2):
    child_schedule = {}
    for course in parent1.schedule.keys():
        if random.random() > 0.5:
            child_schedule[course] = parent1.schedule[course]
        else:
            child_schedule[course] = parent2.schedule[course]
    return Chromosome(child_schedule)

# Mutation
def mutate(chromosome, mutation_rate):
    for course in chromosome.schedule.keys():
        if random.random() < mutation_rate:
            day = random.choice(DAYS)
            timeslot = random.choice(TIMESLOTS)
            classroom = random.choice(CLASSROOMS)
            teacher = random.choice(teachers['Names'])
            chromosome.schedule[course] = (day, timeslot, classroom, teacher)
    chromosome.fitness, chromosome.constraints_fulfilled = chromosome.calculate_fitness()

# Genetic Algorithm
def genetic_algorithm(population_size, generations, mutation_rate):
    population = initialize_population(population_size)
    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        population = sorted(new_population, key=lambda x: x.fitness, reverse=True)[:population_size]
        print(f'Generation {generation}: Best Fitness = {population[0].fitness}')
        print(f'Top 3 Individuals: {[chromosome.fitness for chromosome in population[:3]]}')
    return population[0]

# Display the schedule in a table format
def display_schedule(schedule):
    table = []
    for course, details in schedule.items():
        table.append([course, details[0], details[1], details[2], details[3]])
    headers = ["Course Code", "Day", "Time Slot", "Classroom", "Invigilating Teacher"]
    print(tabulate(table, headers, tablefmt="grid"))

# Main function
if __name__ == "__main__":
    best_schedule = genetic_algorithm(population_size=50, generations=100, mutation_rate=0.05)
    print("Best Schedule:")
    display_schedule(best_schedule.schedule)
    print("Fitness Value:", best_schedule.fitness)
    print("Constraints Fulfilled:")
    for constraint in best_schedule.constraints_fulfilled:
        print(f"- {constraint}")