#!/usr/bin/python
from __future__ import print_function
from time import gmtime, strftime
from PIL import Image # Depends on the Pillow lib
from opensimplex import OpenSimplex
import sys
import random
import json

def write_M():
    # write out a primary configuration file
    global SEALEVEL
    global FEATURE_SIZE
    global WATER_LEVEL
    global SIZE
    conf = dict()
    conf['SEALEVEL'] = SEALEVEL
    conf['FEATURE_SIZE'] = FEATURE_SIZE
    conf['WATER_LEVEL'] = WATER_LEVEL
    conf['SIZE'] = SIZE
    with open('data/conf.json','w') as filehandle:
        json.dump(conf,filehandle,indent=4)

def write_D():
    global MOVE_NW
    global MOVE_N
    global MOVE_NE
    global MOVE_E
    global MOVE_SE
    global MOVE_S
    global MOVE_SW
    global MOVE_W
    with open('data/world1.json','w') as filehandle:
        json.dump(MOVE_NW,filehandle,indent=4)
    with open('data/world2.json','w') as filehandle:
        json.dump(MOVE_N,filehandle,indent=4)
    with open('data/world3.json','w') as filehandle:
        json.dump(MOVE_NE,filehandle,indent=4)
    with open('data/world4.json','w') as filehandle:
        json.dump(MOVE_E,filehandle,indent=4)
    with open('data/world5.json','w') as filehandle:
        json.dump(MOVE_SE,filehandle,indent=4)
    with open('data/world6.json','w') as filehandle:
        json.dump(MOVE_S,filehandle,indent=4)
    with open('data/world7.json','w') as filehandle:
        json.dump(MOVE_SW,filehandle,indent=4)
    with open('data/world8.json','w') as filehandle:
        json.dump(MOVE_W,filehandle,indent=4)

def write_Y():
    global Y
    with open('data/worldY.json','w') as filehandle:
        json.dump(Y,filehandle,indent=4)

def erode():
    global pathx
    global pathz
    global FEATURE_SIZE
    global MAXX
    global MAXZ
    global SEALEVEL
    t=len(pathx)
    c=0
    while ( c < t ):
        erodedist=int(float(FEATURE_SIZE/8))
        erodecount=0
        erodedist1 = random.randint(1,erodedist) # random widths of erosion
        while ( erodecount < erodedist1 ):
            # erode the next space
            # NW,N,NE boundary check
            nw=1
            no=1
            ne=1
            e=1
            se=1
            s=1
            sw=1
            w=1
            if ( pathz[c]-erodecount < 0 ): # skip N directions
                nw=0
                no=0
                ne=0
            if ( pathx[c]-erodecount < 0 ): # skip W directions
                nw=0
                w=0
                sw=0
            if ( pathz[c]+erodecount > MAXZ-1 ): # skip S directions
                se=0
                s=0
                sw=0
            if ( pathx[c]+erodecount > MAXX-1 ): # skip E directions
                ne=0
                e=0
                se=0
            # go NW, N, NE
            # NW
            if ( nw > 0 ):
                terraindiff=int(float((Y[pathx[c]-erodecount][pathz[c]-erodecount]-SEALEVEL)/erodedist))
                Y[pathx[c]-erodecount][pathz[c]-erodecount]=Y[pathx[c]-erodecount][pathz[c]-erodecount]-(terraindiff*erodecount)
            # N
            if ( no > 0 ):
                terraindiff=int(float((Y[pathx[c]][pathz[c]-erodecount]-SEALEVEL)/erodedist))
                Y[pathx[c]][pathz[c]-erodecount]=Y[pathx[c]][pathz[c]-erodecount]-(terraindiff*erodecount)
            # NE
            if ( ne > 0 ):
                terraindiff=int(float((Y[pathx[c]+erodecount][pathz[c]-erodecount]-SEALEVEL)/erodedist))
                Y[pathx[c]+erodecount][pathz[c]-erodecount]=Y[pathx[c]+erodecount][pathz[c]-erodecount]-(terraindiff*erodecount)
            # E
            if ( e > 0 ):
                terraindiff=int(float((Y[pathx[c]+erodecount][pathz[c]]-SEALEVEL)/erodedist))
                Y[pathx[c]+erodecount][pathz[c]]=Y[pathx[c]+erodecount][pathz[c]]-(terraindiff*erodecount)
            # SE
            if ( se > 0 ):
                terraindiff=int(float((Y[pathx[c]+erodecount][pathz[c]+erodecount]-SEALEVEL)/erodedist))
                Y[pathx[c]+erodecount][pathz[c]+erodecount]=Y[pathx[c]+erodecount][pathz[c]+erodecount]-(terraindiff*erodecount)
            # S
            if ( s > 0 ):
                terraindiff=int(float((Y[pathx[c]][pathz[c]+erodecount]-SEALEVEL)/erodedist))
                Y[pathx[c]][pathz[c]+erodecount]=Y[pathx[c]][pathz[c]+erodecount]-(terraindiff*erodecount)
            # SW
            if ( sw > 0 ):
                terraindiff=int(float((Y[pathx[c]-erodecount][pathz[c]+erodecount]-SEALEVEL)/erodedist))
                Y[pathx[c]-erodecount][pathz[c]+erodecount]=Y[pathx[c]-erodecount][pathz[c]+erodecount]-(terraindiff*erodecount)
            # W
            if ( w > 0 ):
                terraindiff=int(float((Y[pathx[c]-erodecount][pathz[c]]-SEALEVEL)/erodedist))
                Y[pathx[c]-erodecount][pathz[c]]=Y[pathx[c]-erodecount][pathz[c]]-(terraindiff*erodecount)
            erodecount=erodecount+1
        c=c+1

def addrivers(seed):
    # how many rivers depends on size? every 100, do 1?
    global SIZE
    global FEATURE_SIZE
    global pathx
    global pathz
    global Y
    n=dict()
    random.seed(seed)
    count = float(SIZE) / 100
    if ( count < 1 ):
        river_count = 1
    else:
        river_count = int(count)
    print("Rivers to make: "+str(river_count)+".")
    sofar = 0
    divergent=FEATURE_SIZE
    while ( sofar < river_count ):
        startx=random.randint(1,SIZE-1)
        startz=random.randint(1,SIZE-1)
        riverlen=random.randint(2,int(SIZE*2))
        print("River start:"+str(sofar)+" from ["+str(startx)+"x"+str(startz)+"] length of "+str(riverlen)+".")
        cx=startx
        cz=startz
        Y[cx][cz]=SEALEVEL
        riversize=0
        prevdir=0
        # follow river
        while ( riversize != riverlen ):
            n=nextnode(cx,cz,prevdir)
            cx=n['x']
            cz=n['z']
            prevdir=n['d']
            Y[cx][cz]=SEALEVEL
            pathx.append(cx)
            pathz.append(cz)
            riversize=riversize+1
        print("Eroding..river. Length: "+str(len(pathx))+".")
        print_river(pathx,pathz)
        erode()
        print("Eroding..Done")
        sofar = sofar+1

def nextnode(x1,z1,nextdir):
    n=dict()
    # go the general direction, but randomly go another (or if this is a new river)
    if ( random.randint(0,100) < 2 or nextdir == 0 ):
        nextdir = random.randint(1,8)
    if ( nextdir == 1 ): # nw
        if ( x1 > 1 and z1 > 1 ):
            n['x']=x1-1
            n['z']=z1-1
            n['d']=1
            return n
        else:
            n['x']=x1+1
            n['z']=z1+1
            n['d']=5
            return n
    elif ( nextdir == 2 ): # no
        if ( z1 > 1 ):
            n['x']=x1
            n['z']=z1-1
            n['d']=2
            return n
        else:
            n['x']=x1
            n['z']=z1+1
            n['d']=6
            return n
    elif ( nextdir == 3 ): # ne
        if ( x1 < MAXX-1 and z1 > 1 ):
            n['x']=x1+1
            n['z']=z1-1
            n['d']=3
            return n
        else:
            n['x']=x1-1
            n['z']=z1+1
            n['d']=7
            return n
    elif ( nextdir == 4 ): # e
        if ( x1 < MAXX-1 ):
            n['x']=x1+1
            n['z']=z1
            n['d']=4
            return n
        else:
            n['x']=x1-1
            n['z']=z1
            n['d']=8
            return n
    elif ( nextdir == 5 ): # se
        if ( x1 < MAXX-1 and z1 < MAXZ-1 ):
            n['x']=x1+1
            n['z']=z1+1
            n['d']=5
            return n
        else:
            n['x']=x1-1
            n['z']=z1-1
            n['d']=1
            return n
    elif ( nextdir == 6 ): # s
        if ( z1 < MAXZ-1 ):
            n['x']=x1
            n['z']=z1+1
            n['d']=6
            return n
        else:
            n['x']=x1
            n['z']=z1-1
            n['d']=2
            return n
    elif ( nextdir == 7 ): # sw
        if ( x1 > 1 and z1 < MAXZ-1 ):
            n['x']=x1-1
            n['z']=z1+1
            n['d']=7
            return n
        else:
            n['x']=x1+1
            n['z']=z1-1
            n['d']=3
            return n
    elif ( nextdir == 8 ): # w
        if ( x1 > 1 ):
            n['x']=x1-1
            n['z']=z1
            n['d']=8
            return n
        else:
            n['x']=x1+1
            n['z']=z1
            n['d']=4
            return n
    print("ERROR: how did we get here: cx="+str(cx)+" cz="+str(cz)+" prevdir="+prevdir+".")
    n['x']=int(SIZE/2)
    n['z']=int(SIZE/2)
    n['d']=0
    return n

def print_river(X,Z):
    start=len(X)
    count=0
    while ( count < start ):
        count=count+1

def drunkpath(sx,sz):
    # find a path from sx,sz to ex,ez the lazy way
    global SEALEVEL
    global Y
    global pathx
    global pathz
    n = dict()
    n['x']=sx
    n['z']=sz
    count=0
    cx=sx
    cz=sz
    px=500
    pz=500
    while ( Y[cx][cz] > SEALEVEL and not (cx == px and cz == pz)):
        #n=nextnode(cx,cz,nextdir)
        px=cx
        pz=cz
        n=lowestnode(cx,cz)
        pathx.append(n['x'])
        pathz.append(n['z'])
        cx = n['x']
        cz = n['z']
        count = count+1


def createfiletext(filename):
    global SEALEVEL
    tad=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fileout = open(filename,"w")
    fileout.write("Displaying the world in ASCII low resolution...\n")
    fileout.write("LEGEND:\n")
    fileout.write(" water is ~\n")
    fileout.write("   0 -  25 = [ ]\n")
    fileout.write("  26 -  50 = [.]\n")
    fileout.write("  51 -  75 = [,]\n")
    fileout.write("  76 - 100 = [-]\n")
    fileout.write(" 101 - 125 = [+]\n")
    fileout.write(" 126 - 150 = [*]\n")
    fileout.write(" 151 - 175 = [%]\n")
    fileout.write(" 176 - 200 = [@]\n")
    fileout.write(" 201 - 225 = [#]\n")
    fileout.write(" 226 - 250 = [^]\n")
    for Z in range(MAXZ):
        for X in range(MAXX):
            V = Y[X][Z]
            if ( V < SEALEVEL+1 ):
                fileout.write('~')
                continue
            if ( V < 26 ):
                fileout.write(' ')
                continue
            if ( V < 51 ):
                fileout.write('.')
                continue
            if ( V < 76 ):
                fileout.write(',')
                continue
            if ( V < 101 ):
                fileout.write('-')
                continue
            if ( V < 126 ):
                fileout.write('+')
                continue
            if ( V < 151 ):
                fileout.write('*')
                continue
            if ( V < 176 ):
                fileout.write('%')
                continue
            if ( V < 201 ):
                fileout.write('@')
                continue
            if ( V < 226 ):
                fileout.write('#')
                continue
            fileout.write('^')
        fileout.write("\n")

def createfileppm(filename):
    tad=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fileout = open(filename,"w")
    fileout.write("P3\n")
    fileout.write("# created as "+filename+" at "+tad+"\n")
    fileout.write(str(MAXX)+"\n")
    fileout.write(str(MAXZ)+"\n")
    fileout.write("85\n")
    for z in range(MAXZ):
        line=""
        for x in range(MAXX):
            # each number is a red/green/blue value. 85 per.
            # < 86 = blue value of blue
            # 86 < 171 =  (subtract 85) = green value
            # > 170 = ( -170) red value
            V = Y[x][z]
            if ( V < 86 ):
                # it is blue, just print it
                line = line+str(0)+" "+str(0)+" "+str(V)+" "
                continue
            if ( V < 171 ):
                V = V-85
                line = line+str(0)+" "+str(V)+" "+str(0)+" "
                continue
            V=V-170
            line = line+str(V)+" "+str(V)+" "+str(V)+" "
        fileout.write(line+"\n")

def createfilepgm(filename,maxy):
    tad=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fileout = open(filename,"w")
    fileout.write("P2\n")
    fileout.write("# created as "+filename+" at "+tad+"\n")
    fileout.write(str(MAXX)+"\n")
    fileout.write(str(MAXZ)+"\n")
    fileout.write(str(maxy)+"\n")
    for z in range(MAXZ):
        line=""
        for x in range(MAXX):
            line = line+str(Y[x][z])+" "
        fileout.write(line+"\n")
    fileout.write("# closed\n")
    fileout.close()

def display_cell(x,z,sl):
    print("Area around "+str(x)+" x "+str(z))
    if ( x > MAXX-3 or x < 0 or z > MAXZ-3 or z < 0 ):
        print("That area cannot be diplayed.")
        return 0
    print("%03d [%03d] | %03d [%03d] | %03d [%03d]" %
            ( Y[x-1][z-1], MOVE_NW[x][z], Y[x][z-1], MOVE_N[x][z], Y[x+1][z-1], MOVE_NE[x][z] ) )
    print("----------+-----------+----------")
    print("%03d [%03d] | %03d [%03d] | %03d [%03d]" %
            ( Y[x-1][z], MOVE_W[x][z], Y[x][z], 0, Y[x+1][z], MOVE_E[x][z] ) )
    print("----------+-----------+----------")
    print("%03d [%03d] | %03d [%03d] | %03d [%03d]" %
            ( Y[x-1][z+1], MOVE_SW[x][z], Y[x][z+1], MOVE_S[x][z], Y[x+1][z+1], MOVE_SE[x][z] ) )
    if ( z > 2 and z < MAXZ-3 ):
        if ( x > 2 and x < MAXX-3 ):
            for Z in range(z-2,z+3):
                print("] Row "+str(Z)+" ",sep=' ',end="")
                for X in range(x-2,x+3):
                    V = Y[X][Z]
                    if ( V < sl+1 ):
                        print('~',end="")
                        continue
                    if ( V < 26 ):
                        print(' ',end="")
                        continue
                    if ( V < 51 ):
                        print('.',end="")
                        continue
                    if ( V < 76 ):
                        print(',',end="")
                        continue
                    if ( V < 101 ):
                        print('-',end="")
                        continue
                    if ( V < 126 ):
                        print('+',end="")
                        continue
                    if ( V < 151 ):
                        print('*',end="")
                        continue
                    if ( V < 176 ):
                        print('%',end="")
                        continue
                    if ( V < 201 ):
                        print('@',end="")
                        continue
                    if ( V < 226 ):
                        print('#',end="")
                        continue
                    print('^',end="")
                print("")
        else:
            print("too close to top or bottom to display")
    else:
        print("too close to left or right")

def calmove(herex,herez,dr):
    global Y
    here=Y[herex][herez]
    done=0
    if ( dr == 1 and herex > 1 and herez > 1 ):
        there=Y[herex-1][herez-1]
        done=1
    if ( dr == 2 and herez > 1 ):
        there=Y[herex][herez-1]
        done=1
    if ( dr == 3 and herex < MAXX-1 and herez > 1 ):
        there=Y[herex+1][herez-1]
        done=1
    if ( dr == 4 and herex < MAXX-1 ):
        there=Y[herex+1][herez]
        done=1
    if ( dr == 5 and herex < MAXX-1 and herez < MAXZ-1 ):
        there=Y[herex+1][herez+1]
        done=1
    if ( dr == 6 and herez < MAXZ-1 ):
        there=Y[herex][herez+1]
        done=1
    if ( dr == 7 and herex > 1 and herez < MAXZ-1 ):
        there=Y[herex-1][herez+1]
        done=1
    if ( dr == 8 and herex > 1 ):
        there=Y[herex-1][herez]
        done=1
    if ( done == 0 ):
        return False
    if ( there > here ):
        if ( dr == 1 or dr == 3 or dr == 5 or dr == 7 ):
            return 14
        if ( dr == 2 or dr == 4 or dr == 6 or dr == 8 ):
            return 10
    if ( there < here ):
        df=abs(there-here)
        mx=int(df/10)
        if ( mx == 0 ):
            mx=1
        mx=mx*2
        # for every 10 more than the local area add 2 points mx=mx*2 then 10 or 14 + mx
        if ( dr == 1 or dr == 3 or dr == 5 or dr == 7 ):
            return 14+mx
        if ( dr == 2 or dr == 4 or dr == 6 or dr == 8 ):
            return 10+mx
    if ( there == here ):
        if ( dr == 1 or dr == 3 or dr == 5 or dr == 7 ):
            return 14
        if ( dr == 2 or dr == 4 or dr == 6 or dr == 8 ):
            return 10

def normalize_around(cx,cz):
    # A=cx-1,cZ-1 B=cX,cZ-1 C=cX+1,cZ-1
    # D=cx-1,cZ   E=cX,cZ   F=cX+1,cZ
    # G=cx-1,cZ+1 H=cX,cZ+1 I=cX+1,cZ+1
    varuse = []
    #if ( cx == 0 ):
    #    return 9
    #if ( cx == MAXX ):
    #    return 9
    #if ( cz == 0 ):
    #    return 9
    #if ( cz == MAXZ ):
    #    return 9
    nwx = cx - 1
    nwz = cz - 1
    if ( nwx > 0 and nwz > 0 and nwx < MAXX and nwz < MAXZ ):
        A = int(Y[nwx][nwz])
        varuse.append(A)
    nx  = cx
    nz  = cz - 1
    if ( nx > 0 and nz > 0 and nx < MAXX and nz < MAXZ ):
        B = int(Y[nx][nz])
        varuse.append(B)
    nex = cx + 1
    nez = cz - 1
    if ( nex > 0 and nez > 0 and nex < MAXX and nez < MAXZ ):
        C = int(Y[nex][nez])
        varuse.append(C)
    wx  = cx - 1
    wz  = cz
    if ( wx > 0 and wz > 0 and wx < MAXX and wz < MAXZ ):
        D = int(Y[wx][wz])
        varuse.append(D)
    # cx = cx
    # cz = cz
    E = int(Y[cx][cz])
    varuse.append(E)
    ex  = cx + 1
    ez  = cz
    if ( ex > 0 and ez > 0 and ex < MAXX and ez < MAXZ ):
        F = int(Y[ex][ez])
        varuse.append(F)
    swx = cx - 1
    swz = cz + 1
    if ( swx > 0 and swz > 0 and swx < MAXX and swz < MAXZ ):
        G = int(Y[swx][swz])
        varuse.append(G)
    sx  = cx
    sz  = cz + 1
    if ( sx > 0 and sz > 0 and sx < MAXX and sz < MAXZ ):
        H = int(Y[sx][sz])
        varuse.append(H)
    sex = cx + 1
    sez = cz + 1
    if ( sex > 0 and sez > 0 and sex < MAXX and sez < MAXZ ):
        I = int(Y[sex][sez])
        varuse.append(I)
    return sum(varuse) / len(varuse)

def main():
    global SEALEVEL
    global FEATURE_SIZE
    global WATER_LEVEL
    global SIZE
    global pathx
    global pathz
    MIN=500
    MAX=0
    CNT=0
    TOT=0
    pathx = []
    pathz = []

    if ( len(sys.argv) > 1 ):
        if ( sys.argv[1] ):
            SIZE=int(sys.argv[1])
        else:
            SIZE=1000
        if ( sys.argv[2] ):
            SEED=int(sys.argv[2])
        else:
            SEED=0
        if ( sys.argv[3] ):
            WATER_LEVEL=float(sys.argv[3])
        else:
            WATER_LEVEL=15.0
        if ( sys.argv[4] ):
            FEATURE_SIZE=float(sys.argv[4])
        else:
            FEATURE_SIZE=24.0
    else:
        SIZE=1000
        SEED=0
        WATER_LEVEL=15.0
        FEATURE_SIZE=24.0
    print("Generating world of size "+str(SIZE)+" by "+str(SIZE)+"...")
    print("Seed "+str(SEED)+" Water Percentage "+str(WATER_LEVEL)+" Land Feature Variant "+str(FEATURE_SIZE)+".")
    global MAXX
    MAXX=SIZE
    global MAXZ
    MAXZ=SIZE
    global Y
    Y = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_NW
    MOVE_NW = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_N
    MOVE_N  = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_NE
    MOVE_NE = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_E
    MOVE_E  = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_SE
    MOVE_SE = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_S
    MOVE_S  = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_SW
    MOVE_SW = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global MOVE_W
    MOVE_W  = [[0 for x in range(MAXX)] for z in range(MAXZ)]
    global SEEDS
    SEEDS   = [[random.randint(0,SIZE) for x in range(MAXX)] for z in range(MAXZ)]

    simplex = OpenSimplex(seed=SEED)
    for z in range(0, MAXX):
        for x in range(0, MAXZ):
            value = simplex.noise3d(x / FEATURE_SIZE, z / FEATURE_SIZE, 0.0)
            y = int((value + 1) * 128)
            if ( y > MAX ):
                MAX=y
            if ( y < MIN ):
                MIN=y
            Y[x][z] = y

    SEALEVEL=int((MAX-MIN)*(WATER_LEVEL/100))+MIN
    print("Make water level "+str(SEALEVEL)+" or below..")
    # waterify W by displaying everything below SEALEVEL+1 as ~

    # calculate movement costs in all direction for W but only above SEALEVEL
    for Z in range(MAXZ):
        for X in range(MAXX):
            if ( Y[X][Z] > SEALEVEL ):
                # process movement
                # MOVE_NW[X][Z] = calmove(X,Z,1)
                # MOVE_N[X][Z]  = calmove(X,Z,2)
                # MOVE_NE[X][Z] = calmove(X,Z,3)
                # MOVE_E[X][Z]  = calmove(X,,Z,4)
                # MOVE_SE[X][Z] = calmove(X,Z,5)
                # MOVE_S[X][Z]  = calmove(X,Z,6)
                # MOVE_SW[X][Z] = calmove(X,Z,7)
                # MOVE_W[X][Z]  = calmove(X,Z,8)
                # special cases, corners and X=MAXX, Z=MAXZ
                if ( X == 0 ):
                    # process N, NE, E, SE, S
                    if ( Z == 0 ):
                        # process E, SE, S
                        MOVE_NW[X][Z] = MOVE_N[X][Z] = MOVE_NE[X][Z] = MOVE_W[X][Z] = MOVE_SW[X][Z] = False
                        MOVE_E[X][Z]  = calmove(X,Z,4)
                        MOVE_SE[X][Z] = calmove(X,Z,5)
                        MOVE_S[X][Z]  = calmove(X,Z,6)
                        continue
                    if ( Z == MAXZ ):
                        # BOTTOM LEFT CORNER, no   process S, SW, W
                        MOVE_W[X][Z]  = MOVE_NW[X][Z] = MOVE_SE[X][Z] = MOVE_S[X][Z] = MOVE_SW[X][Z] = False
                        MOVE_NE[X][Z]  = calmove(X,Z,3)
                        MOVE_N[X][Z] = calmove(X,Z,2)
                        MOVE_E[X][Z]  = calmove(X,Z,4)
                        continue
                    # X is 0 moving down left edge of world, no NW, SW, W
                    MOVE_NW[X][Z] = False
                    MOVE_N[X][Z]  = calmove(X,Z,2)
                    MOVE_NE[X][Z] = calmove(X,Z,3)
                    MOVE_E[X][Z]  = calmove(X,Z,4)
                    MOVE_SE[X][Z] = calmove(X,Z,5)
                    MOVE_S[X][Z]  = calmove(X,Z,6)
                    MOVE_SW[X][Z] = MOVE_W[X][Z]  = False
                if ( X == MAXX ):
                    if ( Z == 0 ):
                        # TOP RIGHT CORNER, no NW, N, NE, E, SE
                        MOVE_NW[X][Z]  = MOVE_N[X][Z] = MOVE_NE[X][Z] = MOVE_E[X][Z] = MOVE_SE[X][Z] = False
                        MOVE_S[X][Z]  = calmove(X,Z,6)
                        MOVE_SW[X][Z] = calmove(X,Z,7)
                        MOVE_W[X][Z]  = calmove(X,Z,8)
                        continue
                    if ( Z == MAXZ ):
                        # BOTTOM RIGHT CORNER, no NE, E, SE, S, SW
                        MOVE_NW[X][Z] = calmove(X,Z,1)
                        MOVE_N[X][Z]  = calmove(X,Z,2)
                        MOVE_NE[X][Z] = MOVE_E[X][Z]  = MOVE_SE[X][Z] = MOVE_S[X][Z]  = MOVE_SW[X][Z] = False
                        MOVE_W[X][Z]  = calmove(X,Z,8)
                        continue
                    # X is MAXX moving down right edge of world, no NE, E, SE
                    MOVE_NW[X][Z] = calmove(X,Z,1)
                    MOVE_N[X][Z]  = calmove(X,Z,2)
                    MOVE_NE[X][Z] = MOVE_E[X][Z]  = MOVE_SE[X][Z] = False
                    MOVE_S[X][Z]  = calmove(X,Z,6)
                    MOVE_SW[X][Z] = calmove(X,Z,7)
                    MOVE_W[X][Z]  = calmove(X,Z,8)
                    continue
                if ( Z == 0 ):
                    # moving across the top, no NW, N, NE
                    MOVE_NW[X][Z] = MOVE_N[X][Z]  = MOVE_NE[X][Z] = False
                    MOVE_E[X][Z]  = calmove(X,Z,4)
                    MOVE_SE[X][Z] = calmove(X,Z,5)
                    MOVE_S[X][Z]  = calmove(X,Z,6)
                    MOVE_SW[X][Z] = calmove(X,Z,7)
                    MOVE_W[X][Z]  = calmove(X,Z,8)
                    continue
                if ( Z == MAXZ ):
                    # moving across the bottom, no SE, S, SW
                    MOVE_NW[X][Z] = calmove(X,Z,1)
                    MOVE_N[X][Z]  = calmove(X,Z,2)
                    MOVE_NE[X][Z] = calmove(X,Z,3)
                    MOVE_E[X][Z]  = calmove(X,Z,4)
                    MOVE_SE[X][Z] = MOVE_S[X][Z]  = MOVE_SW[X][Z] = False
                    MOVE_W[X][Z]  = calmove(X,Z,8)
                    continue
                # Special cases done, not near an edge
                MOVE_NW[X][Z] = calmove(X,Z,1)
                MOVE_N[X][Z]  = calmove(X,Z,2)
                MOVE_NE[X][Z] = calmove(X,Z,3)
                MOVE_E[X][Z]  = calmove(X,Z,4)
                MOVE_SE[X][Z] = calmove(X,Z,5)
                MOVE_S[X][Z]  = calmove(X,Z,6)
                MOVE_SW[X][Z] = calmove(X,Z,7)
                MOVE_W[X][Z]  = calmove(X,Z,8)

    addrivers(SEED)

    print('Generated. Normalizing...')
    # normalize W
    for Z in range(MAXZ):
        for X in range(MAXX):
            Y[X][Z] = normalize_around(X,Z)
            V = Y[X][Z]
            if ( MIN > V ):
                MIN=V
            if ( MAX < V ):
                MAX=V
            CNT = CNT + 1
            TOT = TOT + V
    AVG = TOT / CNT 
    print("Normalize results: MAX "+str(MAX)+" MIN "+str(MIN)+" CNT "+str(CNT)+" AVG "+str(AVG))

    display_cell(84,73,SEALEVEL)

    print("Creating map representations:")
    print("PGM world.pgm [",end='')
    createfilepgm("data/world.pgm",MAX)
    print("DONE]")
    print("PPM world.ppm [",end='')
    createfileppm("data/world.ppm")
    print("DONE]")
    print("TEXT world.txt [",end='')
    createfiletext("data/world.txt")
    print("DONE]")
    print("Saving generated world to files.")
    write_Y()
    write_D()
    write_M()

if __name__ == '__main__':
    main()


