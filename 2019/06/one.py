# from https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
# might try to decrease runtime in future, runtime reporting helpful for that
import time
start_time = time.time()

# dumps orbits into list
def file_reader(file_name):
    orbit_map = []
    with open(file_name) as file_pointer:
        while True:
            line = file_pointer.readline()
            if not line:
                break
            orbit_map.append(line[0:8])   # not all of line bc we don't want '\n'
    return orbit_map


# parses orbit_map into a more workable orbit_map and the set of all objects
def orbit_sorter(old_orbit_map):
    objects = set()                      # set to remove duplicates and be fancy
    orbit_map = []
    for orbit in old_orbit_map:
        if orbit != '\n':                # removes newline item from end of list
            orbit_map.append(orbit.replace('\n', ''))

    for orbit in orbit_map:
        x = orbit.split(')')
        for i in range(2):
            objects.add(x[i])

    return orbit_map, objects


# given the base orbit it counts its way up and returns the number of orbits
def orbit_counter_upper(object, orbit_map):
    counter = 0
    one_up = object
    while base_search(one_up, orbit_map) != -1:
        x = base_search(one_up, orbit_map)
        one_up = x[0:3]
        counter += 1
    return counter


# returns base orbit of an object
def base_search(object, orbit_map):
    for orbit in orbit_map:
        if orbit[4:7] == object:
            return orbit
    return -1


# main program
orbit_map = file_reader('input.txt')      # change filename here!
orbit_map, objects = orbit_sorter(orbit_map)
objects.remove('COM')

total_orbits = 0
for object in objects:
    # print("Into all-objects loop (in main)")
    total_orbits += orbit_counter_upper(object, orbit_map)

print('Answer: ', total_orbits)
# see top for time source, mac runtime <80s 
print("--- %s seconds ---" % (time.time() - start_time))

