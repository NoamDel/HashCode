from verify_solution import verify_dataset_validity
from get_avg_map import get_intersection_car_count

"""
street[0] = start intersection
street[1] = destination intersection
street[2] = name
street[3] = length in seconds
"""
def get_averaged_seconds():
    intersects_to_streets = get_intersection_car_count(objects)
    averaged = []
    for intersect in intersects_to_streets:
        # sum_of_cars = sum(intersect.values())
        min_cars = min(intersect.values())
        new_d = {street: int(cars / min_cars) for street, cars in intersect.items()}
        averaged.append(new_d)
    return averaged

def get_intersects_streets():
    intersect_to_streets = [] # index i holds dict of incoming streets to corresponding cars count
    for i in range(num_of_intersections):
        incoming_streets = dict() # street_name -> num of cars
        for street in streets:
            if i == street[1]:
                incoming_streets[street[2]] = 1 # TODO assume each street has one car waiting
        intersect_to_streets.append(incoming_streets)
    return intersect_to_streets

def generate_output(dataset):
    with open(f'outputs/{dataset}_out.txt', 'w') as f:
        f.write(f'{num_of_intersections}\n')
        for i in range(num_of_intersections):
            f.write(f'{i}\n{len(intersects_to_streets[i])}\n')
            streets_to_num_of_cars = intersects_to_streets[i] # dict {'str1': 1, 'str2': 2}
            new_dict = dict(sorted(streets_to_num_of_cars.items(), key=lambda item: item[1], reverse=True))
            for street, num_of_cars in new_dict.items():
                f.write(f'{street} {num_of_cars}\n') # open each street for 'num_of_waiting_cars' seconds

datasets = ['a', 'b', 'c', 'd', 'e', 'f']
# datasets = ['a']
for dataset in datasets:
    objects = verify_dataset_validity(f'datasets/{dataset}.txt')
    num_of_intersections = objects.simulation_data[1]
    cars = objects.cars
    streets = objects.streets
    # intersects_to_streets = get_intersects_streets()
    intersects_to_streets = get_averaged_seconds()
    generate_output(dataset)