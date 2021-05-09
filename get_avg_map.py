from verify_solution import verify_dataset_validity
import logging,sys,os


def get_intersection_car_count(dataset_obj):
    """
    Assumes valid inputs
    Returns a list where each entry is a dict with "street_name":how_many_cars_enter_it
    """
    street_intersections = dict()
    all_inter_count = [dict() for _ in range(dataset_obj.simulation_data[1])]  # number of intersections
    dirty_inter_track = [False for _ in range(len(all_inter_count))]
    for start_inter, end_inter, name_street, t_street in dataset_obj.streets:
        street_intersections[name_street] = (start_inter,end_inter, t_street)
        for intersection in [end_inter]: # set default timings (one second for each incoming street)
            if intersection not in all_inter_count[intersection]:
                all_inter_count[intersection][name_street] = 1
    for car in dataset_obj.cars:
        streets = car[1:]
        for street in streets:
            assert street in street_intersections
            start, end, t_street = street_intersections[street]
            # for intersection in [start,end]:
            for intersection in [end]:
                if street in all_inter_count[intersection]:
                    if dirty_inter_track[intersection]: # if we have a modified timing for this intersection
                        all_inter_count[intersection][street] += 1
                    else: # we have a default timing, so we need to reset it and start modifying it
                        all_inter_count[intersection] = dict()
                        dirty_inter_track[intersection] = True
                        all_inter_count[intersection][street] = 1
                else: # this intersection does not know this street (so probably it's a modified timing)
                    all_inter_count[intersection][street] = 1
    return all_inter_count

def generate_timings(incoming_counts):
    out_file_lines = [len(incoming_counts)]
    for id,intersection in enumerate(incoming_counts):
        out_file_lines.append(id)
        inc_streets_count = len(intersection.keys())
        out_file_lines.append(inc_streets_count)
        for k,v in intersection.items(): # more seconds to incoming streets that have more cars coming
            cur_street_time = max(1,round(float(v)/inc_streets_count))
            out_file_lines.append(f"{k} {cur_street_time}")
    return out_file_lines

if __name__ == '__main__':
    a = r"datasets/a.txt"
    b = r"datasets/b.txt"
    c = r"datasets/c.txt"
    d = r"datasets/d.txt"
    e = r"datasets/e.txt"
    f = r"datasets/f.txt"
    # todo temp for debugging
    a = r"pdf_example\a.txt"
    # a = r"C:\Hashcode\Hashcode\datasets\b.txt"
    sol = r"pdf_example\sol.txt"
    logging.basicConfig(level=logging.INFO)
    for data_set in [a,b,c,d,e,f]:
    # for data_set in [b]:
        dataset_obj = verify_dataset_validity(data_set)
        all_inter_count = get_intersection_car_count(dataset_obj)
        timings = generate_timings(all_inter_count)
        str_timings = [str(line)+"\n" for line in timings]
        out_file_name = os.path.basename(data_set).split('.')
        out_file_name = os.path.join("solutions",out_file_name[0]+'_sol.'+out_file_name[1])
        with open(out_file_name,'w') as sol_fd:
            sol_fd.writelines(str_timings)