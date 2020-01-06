# only keep track of active cells

# will tally up the neighbors of all cells

# set[(int,int)]
alive_coords = set([])

# functional approach which uses more memory, but preserves the previous data.
def sim_step(alive_coords: set) -> set:
    def neighbours(x,y):
        # able to be massively parallel
        # Needlessly complex code. Was playing golf.
        return [(x+x1,y+y1) for x1 in range(-1,2) for y1 in range(-1,2) if not (x1==0 and y1==0)]
    
    def neighbour_counts(alive_coords):
        # memory limited oof
        # xs.groupby(x=>x).select(x=>x.count())
        point_coords = {}
        for x,y in alive_coords:
            for coord in neighbours(x,y):
                if coord not in point_coords:
                    point_coords[coord] = 0
                point_coords[coord] += 1

        return point_coords
  


    next_generation = set([])
    # bounding box
    mx,mn = [], []
    for coord,count in neighbour_counts(alive_coords).items():
        
        if(count == 3 or (count == 2 and coord in alive_coords)):
            next_generation.add(coord)

            # find the bounding box of our world
            if len(mx) == 0:
                # makes mutable
                mx = list(coord)
                mn = list(coord)
            else:
                if mx[0] < coord[0]:
                    mx[0] = coord[0]
                elif mn[0] > coord[0]:
                    mn[0] = coord[0]
                
                if mx[1] < coord[1]:
                    mx[1] = coord[1]
                elif mn[1] > coord[1]:
                    mn[1] = coord[1]

    return (next_generation, mx, mn)


def glider():   
    # x   x
    # x x
    #   x
    return [(0,1),(0,2),(1,0),(1,1),(2,2)]

def box():
    # x x
    # x x
    return [(0,0),(0,1),(1,0),(1,1)]

def blinker():
    #   X
    #   X
    #   X
    return [(1,1),(1,2),(1,0)]

def glider_chaos():   
    # x   x
    # x x
    #   x
    return [(0,1),(0,2),(1,0),(1,1),(2,2), (-5,-5),(-5,-6),(-5,-4)]

alive_coords = glider_chaos() #box() #blinker()
alive_coords = set(alive_coords)

def ascii_print(alive_coords, mx, mn):
    def bool_to_char(b):
        if b:
            return 'X'
        return '-'

    # print world, line by line, localized to an extended bounding box
    for y in range(mn[1]-1,mx[1]+2):
        print(''.join([bool_to_char((x,y) in alive_coords) for x in range(mn[0]-1,mx[0]+2)]))
        
from time import sleep
for step in range(200):
    alive_coords, mx, mn = sim_step(alive_coords)
    ascii_print(alive_coords, mx, mn)
    sleep(0.125)
    print()

print(alive_coords)