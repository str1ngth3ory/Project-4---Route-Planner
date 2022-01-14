from collections import defaultdict
import math

def shortest_path(M, start, goal):
    
    result = str()
    
    # use dictionary to store path cost (g), estimate distance to goal (h), and total cost (f) for easy value lookup
    g = defaultdict(lambda:math.inf)
    h = dict()
    f = defaultdict(lambda:math.inf)
    
    # initialize the data for starting point
    # note: path is stored as string
    frontiers = set({str(start)})
    g[str(start)] = 0
    h[str(start)] = distance(M, start, goal)
    f[str(start)] = g[str(start)] + h[str(start)]

    while frontiers:
        
        # find the path to the target in the frontiers with the smallest total cost
        min_path = None
        
        for path in frontiers:
            if min_path == None:
                min_path = path
            elif f[path] < f[min_path]:
                min_path = path
        
        if f[min_path] >= f[result]:
            break
            
        min_path_list = min_path.split('>>')
        
        # find the next frontiers, calculate and store their costs
        for intersection in M.roads[int(min_path_list[-1])]:
            # check to make sure we are not going backward
            if len(min_path_list) > 1:
                if intersection == int(min_path_list[-2]):
                    continue
            
            new_path = min_path + '>>' + str(intersection)
            frontiers.add(new_path)
            new_path_distance = g[min_path] + distance(M, int(min_path_list[-1]), intersection)
            if g[new_path] > new_path_distance:
                g[new_path] = new_path_distance
            h[new_path] = distance(M, intersection, goal)
            f[new_path] = g[new_path] + h[new_path]
        
        # store the shortest path if goal is reached
        if min_path.endswith(str(goal)):
            if result == '':
                result = min_path
            elif f(min_path) < f(result):
                result = min_path
        
        frontiers.remove(min_path)
        
    return list(map(int, result.split('>>')))

# a function to evaluate distance between two points
# used for calculating point to point path cost and estimated distance to the goal
def distance(M, start, end):
    a = M.intersections[start]
    b = M.intersections[end]
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)