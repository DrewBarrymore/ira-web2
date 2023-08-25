import csv
from licensor.models import Access_key

filenames = [
    '27Two Creative LLP2023_03_13 17:32:01.csv',
]


def load_keys(filename:str):
    try:
        with open(filename, 'r', newline='') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=",")
            rowCount = 0
            for row in csvreader:
                if rowCount > 0:
                    new_key = Access_key(pass_code=row[2], feret_key=row[1], licensed_to=row[0], valid_for_days=row[4], valid_till=row[5], sequence=row[3])
                    new_key.save()
                rowCount += 1
    except Exception as e:
        print(f'Unable to create and load passkey information in django models db--{str(e)}')

# for file in filenames:
#     print(file)
#     load_keys(filename=file)
