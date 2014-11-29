import numpy as np
import matplotlib.pyplot as plt
import itertools  # for cartesian product

MAX_STEPS = 160
steps = range(MAX_STEPS)
cellSize = 0.4 # m
width = 4 # m
height = 4 # m
dim_y = int(width/cellSize) + 2  # add ghost cells
dim_x = int(height/cellSize) + 2 # add ghost cells
OBST = np.ones( (dim_x, dim_y) , int) # obstacles/walls/boundaries
SFF = np.empty( (dim_x, dim_y) ) # static floor field
SFF[:] = np.Inf 

DFF = np.ones( (dim_x, dim_y) ) # dynamic floor field

def init_obstacles():
    pass

def init_walls(exit_cells):
    OBST[0,:]  = OBST[-1,:] = OBST[:,-1] = OBST[:,0] = np.Inf
    for e in exit_cells:
        OBST[e] = 1
    print "walls"
    print OBST
    return OBST

# def init_exits(exit_cells):
#     """
#     needed for ploting
#     """
#     exits =  = np.ones( (dim_x, dim_y) ) # 
#     for e in exit_cells:

#     OBST[0,:]  = OBST[-1,:] = OBST[:,-1] = OBST[:,0] = np.Inf


#holding box
from_x, to_x = 1, 7
from_y, to_y = 1, 7

box = [from_x, to_x, from_y, to_y]

N_pedestrians = 50
nx = to_x - from_x + 1
ny = to_y - from_y + 1
if N_pedestrians > nx*ny:
    N_pedestrians = nx*ny

def init_peds(N, box, width, height, walls):
    """
    distribute N pedestrians in box 
    """
    from_x, to_x = box[:2]
    from_y, to_y = box[2:]
    nx = to_x - from_x + 1
    ny = to_y - from_y + 1
    PEDS = np.ones(N, int) #
    print "box: ",from_x, to_x, from_y, to_y
    print "nx", nx, "ny", ny, "nx*ny", nx*ny, "N", N
    print "PEDS ", PEDS
    
    EMPTY_CELLS_in_BOX = np.zeros( nx*ny - N, int) #
    print "EMPTY_CELLS_in_BOX ", EMPTY_CELLS_in_BOX
    PEDS = np.hstack((PEDS,  EMPTY_CELLS_in_BOX))
    print "hstack PEDS ", PEDS
    np.random.shuffle(PEDS)
    print "shuffle PEDS ", PEDS
    PEDS = PEDS.reshape( (nx,ny) )
    print "reshape PEDS ", PEDS
    print "zeros ", dim_x-nx, dim_y-ny
    EMPTY_CELLS = np.zeros( (dim_x, dim_y), int )
    EMPTY_CELLS [ from_x:to_x+1, from_y:to_y+1  ] = PEDS 
    print "EMPTY_CELLS "
    print EMPTY_CELLS

    return EMPTY_CELLS

# holdingArea_x = int(dim_x * 1) # holding area where we distribute N peds
# holdingArea_y = int(dim_y * 0.5)
# holdingArea = holdingArea_x*holdingArea_y
# PEDS = np.hstack((np.ones( (holdingArea/2) ), np.zeros( (holdingArea/2 +  holdingArea%2) ) ) )

cells_initialised  = [] # list of cells which have their ssf initialized

exit_cells = [ (dim_x/2, dim_y-1) ]

x=0
y=0
leftX = (x - 1 + dim_x) % dim_x
rightX = (x + 1) % dim_x
aboveY = (y - 1 + dim_y) % dim_y
belowY = (y + 1) % dim_y
print leftX 
print (x + 1) % width;
print (y - 1 + height) % height;
print (y + 1) % height;
def plot_sff(walls):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.cla()
    cmap = plt.get_cmap()
    cmap.set_bad(color = 'k', alpha = 0.8)
    vect = SFF*walls
    vect[vect<-10] = np.Inf
    print vect
    ax.imshow(vect, cmap=cmap , interpolation = 'lanczos') #  lanczos nearest

    plt.savefig("SFF.png")
    print "figure: SFF.png"


def plot_peds(peds, walls, i):
    # dt= 0.33
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.cla()
    cmap = plt.get_cmap("gray")
    cmap.set_bad(color = 'b', alpha = 0.8)
    N = np.sum(peds)
    # print peds+walls
    ax.imshow(peds+walls, cmap=cmap, vmin=-1, vmax=2,interpolation = 'nearest') # 1-peds because I want the peds to be black
    S = "t: %3.3d  |  N: %3.3d "%(i,N)
    plt.title("%6s"%S)    
    plt.savefig("peds%.5d.png"%i)
    # print "figure: peds%.5d.png"%i

    

def update_DFF():
    """
    not yet implemented (tricky part!)
    """
    return  np.ones( (dim_x, dim_y) )

def init_SFF():
    #start with exit's cells
    for e in exit_cells:
        cells_initialised.append(e)
        SFF[e] = 0
    
    while cells_initialised:
        cell = cells_initialised.pop(0)
        neighbor_cells = get_neighbors(cell)
        for neighbor in neighbor_cells:
            if SFF[cell] < SFF[neighbor]:
                SFF[neighbor] = SFF[cell] + 1
                cells_initialised.append(neighbor)
    return SFF


def get_neighbors(cell):  # von Neumann neighborhood
    
    neighbors = []
    i = cell[0]
    j = cell[1]
    if i+1 < dim_y:
        neighbors.append( (i+1, j) )
        
    if i-1 >= 0:
        neighbors.append( (i-1, j) )
        
    if j+1 < dim_x:
        neighbors.append( (i, j+1) )
        
    if j-1 >= 0:
        neighbors.append( (i, j-1) )

    return neighbors
        



    
if __name__ == "__main__":
    kappaS = 1
    kappaD = 0
    sff = init_SFF()
    walls = init_walls(exit_cells)
    init_obstacles()
    peds = init_peds(N_pedestrians, [from_x, to_x, from_y, to_y], width, height, walls)
    # print PEDS
    plot_sff(walls)
    exit()
    # to calculate probabilities change values of walls
    prob_walls = np.empty_like (walls)
    plot_walls = np.empty_like (walls)
    # np.copyto(prob_walls, walls) 
    prob_walls[walls != 1] = 0 # not accessible
    prob_walls[walls == 1] = 1 # accessible
    plot_walls[walls != 1] = -10 # not accessible
    plot_walls[walls == 1] = 0 # accessible
    
    print "probwalls"
    print prob_walls
    print "walls"
    print walls
    
    print "sff"
    print sff
    # raw_input()
    for t in steps: # time loop
        plot_peds(peds, plot_walls, t)
        print "---------------------------------"
        print "t: ", t, "N=", np.sum(peds)
        print peds
        print "---------------------------------"
        dff = update_DFF()
        # probability = np.exp(-kappaS*sff)  * (1-peds) * prob_walls  # *np.exp(-kappaD*dff)
        # print probability
        # s = sum(probability)
        tmp_peds = np.empty_like (peds)
        np.copyto(tmp_peds, peds) 
        for (i,j) in itertools.product(range(1,dim_x), range(1,dim_y)):
            cell = [i,j]
            # print "cell", cell, "p[i,j]",peds[i,j] 
            if peds[i,j] == 0  : continue
            p = 0
            probs = {}
            for neighbor in get_neighbors(cell):
                probability = np.exp(-kappaS*sff[neighbor])  * (1-tmp_peds[neighbor]) * prob_walls[neighbor]  # *np.exp(-kappaD*dff)
                # p += probability[neighbor]
                p += probability
                probs[neighbor] = probability
                # print neighbor, " hat prob ",probability[neighbor]
            if p == 0:
                continue
            r = np.random.rand() * p
            # print "r", r
            # print "start update"
            for neighbor in get_neighbors(cell):
                # r -= probs[neighbor]
                r -=  np.exp(-kappaS*sff[neighbor])  * (1-tmp_peds[neighbor]) * prob_walls[neighbor]  # 
                # print "neighbor", neighbor, "prob", probability[neighbor], "r" ,r, r<=0
                if r <= 0: # move to neighbor cell
                    if np.array([set(e)==set(neighbor) for e in exit_cells ] ).any(): # reached exit?
                        # print "exit=neighbor", neighbor
                        # print "cell", cell
                        # raw_input()
                        tmp_peds[i,j] = 0
                    else:
                        # print "ELSE neighbor", neighbor, "prob", probability[neighbor], "r" ,r, r<=0
                        # print "cell", cell, " (",i,j,") moves to", neighbor, "was occupied?",peds[neighbor]
                        tmp_peds[neighbor] = 1
                        tmp_peds[i,j] = 0
                        # raw_input()
                    break
        
        np.copyto(peds, tmp_peds)
        # print tmp_peds
        # raw_input()
        if not peds.any(): # everybody is out
            break

    print "Simulation time: ", t