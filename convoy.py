# Write your code here
import pandas as pd
import csv
import re



def convert_xlxs_to_csv(name):
    xlsx = pd.read_excel(rf'{name[0]}.{name[1]}', sheet_name='Vehicles', dtype=str)
    xlsx.to_csv(name[0] + '.csv', index=False, header=True)
    return len(xlsx)

def lines_counter(name):

    if name[1] == 'xlsx':
        xlsx = pd.read_excel(rf'{name[0]}.{name[1]}', sheet_name='Vehicles', dtype=str)
        return len(xlsx)
    elif name[1] == 'csv':
        None

def csv_writer(file_name, field_names, dict):

    with open(f'{file_name}[CHECKED].csv', "a", encoding='utf-8') as w_file:
        file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\n", fieldnames=field_names)
        file_writer.writeheader()
        file_writer.writerows([dict])





print('Input file name')
user_file_name = input().split('.')   # input().split('.') 'convoy.xlsx'.split('.') data_one_xlsx 'data_one_csv.csv'.split('.')

csv_file_name = None

if user_file_name[1] == 'xlsx':
    convert_xlxs_to_csv(user_file_name)
    csv_file_name = f"{user_file_name[0]}.csv"
else:
    csv_file_name = f"{user_file_name[0]}.csv"

counter_cells = 0
counter_lines = 0

with open(csv_file_name, newline='') as cs:
    file_reader = csv.DictReader(cs, delimiter=",")  # Create a reader object

    for line in file_reader:  # Read each line

        counter_lines += 1
        names = []
        modified_dict = {}
        for key, value in line.items():
            modified_dict[key] = re.search(r'[0-9]+', value).group(0)
            if re.search(r'[a-zA-z.]+', value) is not None:
                counter_cells += 1
            names.append(key)
        csv_writer(user_file_name[0], names, modified_dict)

if lines_counter(user_file_name) is not None:
    if lines_counter(user_file_name) == 1:
        print(f'{lines_counter(user_file_name)} line was added to {user_file_name[0]}.csv')
    elif lines_counter(user_file_name) > 1:
        print(f'{lines_counter(user_file_name)} lines were added to {user_file_name[0]}.csv')
    #
if counter_cells == 1:
    print(f'{counter_cells} cell was corrected in {user_file_name[0]}[CHECKED].csv')
else:
    print(f'{counter_cells} cells were corrected in {user_file_name[0]}[CHECKED].csv')
# csv_file = xlsx_file.to_csv(user_file_name[0] + '.csv', index=False, header=True)
#
# vehicles = pd.read_csv(f'{user_file_name[0]}.csv')
#
# if vehicles.shape[0] > 1:
#      print(f'{vehicles.shape[0]} lines were imported to {user_file_name[0]}.csv')
#
# elif vehicles.shape[0] == 1:
#     print(f'{vehicles.shape[0]} line was imported to {user_file_name[0]}.csv')
