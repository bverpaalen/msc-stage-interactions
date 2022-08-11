import os, csv,copy
import datetime, calendar

csv_dir = "C:\\Users\\user\\Desktop\\Leiden\\Research Project\\experiment\\"
csv_names = ["blue_20191121-143851.csv","orange_20191121-144424.csv","pink_20191121-144621.csv","white_20191121-144124.csv"]

def main(csv_path, dirName="", delim=","):
    if dirName != "":
        try:
            os.mkdir(".\\"+str(dirName))
        except OSError:
            print("Creation of the dir at path %s failed" % os.getcwd())

    csv_file = open(csv_path)
    csv_reader = csv.reader(csv_file,delimiter=delim)


    path = []
    i = 0
    j = 0
    minuteThreshold = 1
    timeThreshold = minuteThreshold * 60

    for row in csv_reader:
        if i < 1:
            i += 1
            continue
        str_date = row[0]
        str_time = row[1]


        date_time = datetime.datetime.strptime(str_date+str_time,"%Y/%m/%d %H:%M:%S")
        unix_time = calendar.timegm(date_time.utctimetuple())

        if len(path) > 0:
            timeDif = abs(unix_time - old_unix_time)

            if timeDif < timeThreshold:
                path.append(row)
            else:
                listToCsv(path,dir_name=dirName,postfix=j)
                j += 1
                path = [row]
            old_unix_time = copy.deepcopy(unix_time)
        elif len(path) == 0:
            path.append(row)
            old_unix_time = copy.deepcopy(unix_time)

        i += 1

def listToCsv(list,dir_name="",postfix=""):

    if dir_name != "":
        dir_name += "\\"

    print("creating csv "+str(postfix))
    if postfix != "":
        postfix = "_" + str(postfix)
    file = open(".\\"+dir_name+"path"+postfix +".csv","w+")
    csv_file = csv.writer(file)
    for row in list:
        sentence = ""
        for object in row:
            sentence += object + ","
        sentence = sentence[:-1]
        sentence += "\n"
        file.write(sentence)
    file.close()
for csv_name in csv_names:
    csv_path = csv_dir + csv_name
    main(csv_path,csv_name.split("_")[0])