import time

lab = [[0 for j in range(40)] for i in range(25)]

for i in range(30):
    lab[0][i]=1

for i in range(10,40):
    lab[9][i]=1

for i in range(30):
    lab[14][i]=1

for i in range(10,40):
    lab[17][i]=1

start_time= time.time()

def print_lab(labirint,start=None,finish=None,way=[]):
    for point in way: labirint[point[0]][point[1]]="*"
    if start is not None: labirint[start[0]][start[1]] = "S"
    if finish is not None: labirint[finish[0]][finish[1]] = "F"
    for i in labirint:
        for j in i:
            print(str(j).rjust(1),end="")
        print()
    
def find_steps(y, x,labirint):
    ways = [-1, 0], [0, -1], [1, 0], [0, 1],[-1,-1],[1, 1],[-1, 1],[1, -1]
    steps=[]
    for dy,dx in ways:
        if (0 <= y+dy < len(labirint) and
            0 <= x+dx < len(labirint[0])
            and labirint[y+dy][x+dx]==0):
            steps.append((y+dy,x+dx))
    return steps
        

def find_way(labirint,start=None,finish=None):
    ways = [-1, 0], [0, -1], [1, 0], [0, 1],[-1,-1],[1, 1],[-1, 1],[1, -1]    
    graph = {}
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if labirint[i][j]==0:
                graph[(i, j)] = find_steps(i, j,labirint)
    n=0
    n_lab=[[-1 for j in i] for i in labirint]
    n_lab[start[0]][start[1]]=n
    finding=True
    while finding and n<len(n_lab)*len(n_lab[0]):
        n+=1
        for i in range(len(n_lab)):
            for j in range(len(n_lab[i])):
                if n_lab[i][j]==n-1:
                    for point in graph[(i, j)]:
                        if n_lab[point[0]][point[1]]==-1:
                            dy = i - point[0]
                            dx = j - point[1]
                            if [dy,dx] in ways[4:]:
                                n_lab[point[0]][point[1]]=n+2
                            else:
                                n_lab[point[0]][point[1]]=n+1
                            if (point[0],point[1])==finish:
                                finding=False           
    #print_lab(n_lab)
    way=[]
    
    if finding: return []
    else:
        way.append(finish)
        curr_point=finish
        while curr_point!=start:
            min_point = 99999
            temp_point=0
            ways = [-1, 0], [0, -1], [1, 0], [0, 1],[-1,-1],[1, 1],[-1, 1],[1, -1]
            for dy,dx in ways:
                if (n_lab[curr_point[0]+dy][curr_point[1]+dx]<
                    n_lab[curr_point[0]][curr_point[1]] and
                    n_lab[curr_point[0]+dy][curr_point[1]+dx]!=-1):
                    if (-1<n_lab[curr_point[0]+dy][curr_point[1]+dx]<min_point):
                        temp_point=(curr_point[0]+dy,curr_point[1]+dx)
                        min_point = n_lab[curr_point[0]+dy][curr_point[1]+dx]
            curr_point=temp_point
            way.append(curr_point)
        way = way[::-1]
        #print(way)
        return way



start_point = (1,5)
finish_point = (20,30)

way = find_way(lab,start_point,finish_point)
print(time.time()-start_time)
print_lab(lab,start_point,finish_point,way)
