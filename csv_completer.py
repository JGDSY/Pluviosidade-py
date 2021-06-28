import csv
import glob

path = "dados_mensais"

all_files = glob.glob(path + "/*.csv")
li = []

#filename = path + "/dados_82024_M_2020-01-01_2020-12-31.csv"

for filename in all_files:
    with open(filename,'r') as f:
        line_count=0
        altitude = 0
        longitude = 0
        latitude = 0
        reader = csv.reader(f,delimiter=';')
        lines = []
        for line in reader:
            if line != []:
                if line_count == 2:
                    latitude = str(line[0])[line[0].find(": ")+2:]
                if line_count == 3:
                    longitude = str(line[0])[line[0].find(": ")+2:]
                if line_count == 4:
                    altitude = str(line[0])[line[0].find(": ")+2:]

                if line_count == 10:
                    line[9] = "latitude"
                    line.append("longitude")
                    line.append("altitude")
                if line_count > 10:
                    line[9] = latitude
                    line.append(longitude)
                    line.append(altitude)
            line_count += 1
            lines.append(line)
            print(line)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(lines)