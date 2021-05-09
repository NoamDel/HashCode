import sys,os,argparse,logging,types

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=str, help='Path to dataset file')
    parser.add_argument('solution', type=str, help='Path to solution file')
    args = parser.parse_args()
    data_path = args.data
    solution_path = args.solution
    if not os.path.isfile(data_path) or not os.path.isfile(solution_path):
        raise Exception(f"At least one of the given paths does not exist:\n\tdataset: {data_path}\n\tsolution: {solution_path}")
    return data_path,solution_path

def verify_dataset_validity(dataset_path):
    """
    Returns None if there's a problem in the file (or something failed to parse).
    If all is valid, returns the following namespace:
    output.simulation_data = the first line of the file that details the simulation
    output.streets = a list of the street definitions
    output.cars = a list of the car definitions
    """
    assert os.path.isfile(dataset_path)
    logging.info(f"Validating dataset at {dataset_path}")
    with open(dataset_path,'r') as dataset_fd:
        dataset_lines = dataset_fd.readlines()
    # first line should be: t_sim n_inter n_street n_cars car_score
    if len(dataset_lines) <= 0: # an empty file is invalid
        logging.warning("Empty dataset file")
        return None
    lines_iter = iter(dataset_lines)
    try:
        line = next(lines_iter)
        first_line_split = [int(item) for item in line.split()]
    except Exception as e:
        logging.warning(f"Failed to parse line {line}:\n{e}")
        return None
    if len(first_line_split) != 5:
        logging.warning(f"Line {line} as less than 5 items")
        return None
    t_sim, n_inter, n_street, n_cars, car_score = first_line_split
    output = types.SimpleNamespace(simulation_data=[t_sim, n_inter, n_street, n_cars, car_score],
                                   streets= [],
                                   cars = [])
    if not len(dataset_lines) == 1 + n_street + n_cars: # as per specification pdf
        logging.warning(f"Dataset doesn't have correct number of lines (1 + n_street + n_cars = {1 + n_street + n_cars} but data set length is {len(dataset_lines)}")
        return None
    for _ in range(n_street):
        line = next(lines_iter)
        cur_street_split = line.split()
        if len(cur_street_split) != 4:
            logging.warning(f"Line {line} as less than 4 items")
            return None
        try:
            start_inter, end_inter, t_street = [int(item) for item in cur_street_split[:2]+[cur_street_split[3]]]
        except Exception as e:
            logging.warning(f"Failed to parse line {line}:\n{e}")
            return None
        name_street = cur_street_split[2]
        output.streets.append([start_inter, end_inter, name_street, t_street])
    for _ in range(n_cars):
        cur_car_split = next(lines_iter).split()
        try:
            path_len = int(cur_car_split[0])
            if len(cur_car_split[1:]) != path_len:
                logging.warning(f"Current car's path is of incorrect length (expected {path_len} but got {len(cur_car_split[1:])})")
                return None
        except Exception as e:
            logging.warning(f"Failed to parse line {line}:\n{e}")
            return None
        output.cars.append([path_len]+cur_car_split[1:])
    return output

def verify_solution_validity(solution_path):
    """
    Returns None if there's a problem in the file (or something failed to parse).
    If all is valid, returns the following namespace:
    output.number_of_intersections = the number of intersections in the solution
    output.intersections = a list of the intersection definitions
    """
    assert os.path.isfile(solution_path)
    logging.info(f"Validating solution at {solution_path}")
    with open(solution_path,'r') as solution_fd:
        solution_lines = solution_fd.readlines()
    # first line should be: A = number of intersections
    if len(solution_lines) <= 0: # an empty file is invalid
        logging.warning("Empty dataset file")
        return None
    try:
        line = solution_lines[0]
        n_inter = int(line)
    except Exception as e:
        logging.warning(f"Failed to parse first line {line}:\n{e}")
        return None
    if n_inter == 0:
        return None
    if n_inter < 0:
        logging.warning(f"Invalid number of intersections in first line of file ({n_inter})")
        return None
    output = types.SimpleNamespace(number_of_intersections=n_inter,
                                   intersections = [])
    cur_line = 1
    while cur_line < len(solution_lines):
        try:
            inter_id = int(solution_lines[cur_line])
            cur_line += 1
            E_I = int(solution_lines[cur_line])
            streets = []
            cur_line += 1
            for _ in range(E_I):
                street_name, duration = solution_lines[cur_line].split()
                streets.append([street_name,duration])
                cur_line += 1
            output.intersections.append([inter_id,E_I, streets])
        except Exception as e:
            logging.warning(f"Failed to parse line {cur_line} ({solution_lines[cur_line]}) of solution file:\n{e}")
            return None
    return output


if __name__ == '__main__':
    # data_path,solution_path = parse_args()

    # todo temp for debugging
    a = r"pdf_example\a.txt"
    sol = r"pdf_example\sol.txt"
    sol = r"solutions/b_sol.txt"
    logging.basicConfig(level=logging.INFO)
    dataset_obj = verify_dataset_validity(a)
    if dataset_obj is None:
        logging.fatal(f"Dataset at {a} is invalid, see logs for details...")
        exit(-1)
    solution_obj = verify_solution_validity(sol)
    print(solution_obj)


