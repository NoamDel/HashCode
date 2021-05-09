from verify_solution import verify_dataset_validity

"""
3 - There are 3 intersections with traffic light schedules
1 - intersection 1
2 - 2 streets with green light
rue-d-athenes 2 - street, seconds
rue-d-amsterdam 1
0 - intersection 0
1 - 1 street with green light
rue-de-londres 2
2
1
rue-de-moscou 1
"""

def get_first_incoming_street(intersection_num):
    for street in streets:
        if street[1] == intersection_num:
            return street[2]

def generate_output(dataset):
    with open(f'trivial_outputs/{dataset}_out.txt', 'w') as f:
        f.write(f'{num_of_intersections}\n')
        for i in range(num_of_intersections):
            open_street = get_first_incoming_street(i)
            f.write(f'{i}\n1\n{open_street} 1\n')

for dataset in ['a', 'b', 'c', 'd', 'e', 'f']:
    objects = verify_dataset_validity(f'datasets/{dataset}.txt')
    num_of_intersections = objects.simulation_data[1]
    cars = objects.cars
    streets = objects.streets
    generate_output(dataset)

