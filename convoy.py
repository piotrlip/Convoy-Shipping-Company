# Write your code here
import pandas as pd
import csv
import re
import sqlite3
import json


# def create_connection(db_file):
#     db_name = db_file.replace('[CHECKED]', '')
#     conn = sqlite3.connect(db_name)
#     return conn


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
    with open(f'{file_name}[CHECKED].csv', "w", encoding='utf-8') as w_file:
        file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\n", fieldnames=field_names)
        file_writer.writeheader()
        file_writer.writerows(dict)
    w_file.close()


def checking_file_name(name):
    check = re.search(r'CHECKED', name[0])

    if check is None:
        return True
    else:
        return False


def create_table(file_name):
    db_name = file_name[0].replace('[CHECKED]', '')
    conn = sqlite3.connect(f'{db_name}.s3db')
    c = conn.cursor()
    data_open = open(f'{file_name[0]}.{file_name[1]}', 'r')
    data_to_write = [line.split(',') for line in data_open]

    create_table_sql = f""" CREATE TABLE IF NOT EXISTS 
                    convoy (
                            {data_to_write[0][0]} INTEGER PRIMARY KEY ,
                            {data_to_write[0][1]} INTEGER NOT NULL,
                            {data_to_write[0][2]} INTEGER NOT NULL, 
                            {data_to_write[0][3]} INTEGER NOT NULL 
                            )"""

    c.execute(create_table_sql)
    conn.commit()

    count_records = 0
    for element in data_to_write[1:]:
        insert_data_sql = f"""INSERT INTO convoy(
                                                    {data_to_write[0][0]} , 
                                                    {data_to_write[0][1]} , 
                                                    {data_to_write[0][2]} , 
                                                    {data_to_write[0][3]} )
                            VALUES(
                                                    '{element[0]}', 
                                                    '{element[1]}', 
                                                    '{element[2]}', 
                                                    '{element[3]}') """

        c.execute(insert_data_sql)
        conn.commit()
        count_records += 1
    conn.close()

    if count_records == 1:
        return f'{count_records} record was inserted into {db_name}.s3db'
    else:
        return f'{count_records} records were inserted into {db_name}.s3db'

def convert_to_json():
    pass


print('Input file name')
user_file_name = input().split('.')  # input().split('.') 'convoy.xlsx'.split('.') data_one_xlsx 'data_one_csv.csv'.split('.') 'data_big_xlsx[CHECKED].csv'

task = checking_file_name(user_file_name)

if task is True:

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

        names = []
        modified_dict_list = []
        for line in file_reader:  # Read each line

            counter_lines += 1
            row_dict = {}

            for key, value in line.items():
                row_dict[key] = re.search(r'[0-9]+', value).group(0)
                if re.search(r'[a-zA-z.]+', value) is not None:
                    counter_cells += 1
                if key not in names:
                    names.append(key)
            modified_dict_list.append(row_dict)
    csv_writer(user_file_name[0], names, modified_dict_list)

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

    new_table = create_table(f'{user_file_name[0]}[CHECKED].csv'.split('.'))
    print(new_table)

else:

    new_table = create_table(user_file_name)
    print(new_table)

