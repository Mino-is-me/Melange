import csv
import os

filename = "PresetManager/mapping/DT_CP.csv"
data = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        data.append(row)
        from_folder = "D:/vs/Melange/PresetManager/mapping/from"
        to_folder = "D:/vs/Melange/PresetManager/mapping/to"
        file_names = os.listdir(from_folder)
 
        for file_name in file_names:
            isFile = file_name.find(row[0])
            if isFile != -1:
                new_file_name = file_name.replace(row[0], row[1])
                new_file_path = os.path.join(to_folder, new_file_name)
                file_path = os.path.join(from_folder, file_name)
                if not os.path.exists(new_file_path):
                    os.rename(file_path, new_file_path)
