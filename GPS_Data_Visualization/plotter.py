import os

#import matplotlib
#matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

dirs = ["blue","orange","pink","white"]

def main(dir):
    files = allFiles(dir)
    i=0
    for file in files:
        num = int(file.split("_")[1].split(".")[0])

        lats,longs = extractCoordinates("./"+dir+"/"+file)
        plot(longs,lats,num,dir)

def allFiles(dir, extension=".csv"):
    files = []
    for file in os.listdir(dir):
        if file.endswith(extension):
            files.append(file)
    return files

def extractCoordinates(path,delim=","):
    file = open(path,"r+")
    lats = []
    longs = []
    first = True

    for line in file:

        if first:
            first = False
            continue

        data = line.split(delim)
        lat = float(data[2].replace(" ",""))
        long = float(data[3].replace(" ",""))
        lats.append(lat)
        longs.append(long)
    file.close()
    return lats,longs

def plot(Xs,Ys,num="1337",dir=""):
    if dir != "":
        prefix = dir+"_"

    pName = prefix+"plot_"+str(num)

    plt.plot(Xs,Ys)

    plt.savefig(dir+"/"+pName)
    plt.clf()
for dir in dirs:
    main(dir)