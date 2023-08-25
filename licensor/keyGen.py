from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os
import csv

class keyGen:
    """Generating license keys client name, license type etc in cipher itself"""

    def __init__(self, key=""):
        self.key = key
        self.plainText = None
        self.cipherText = None
        self.fernet = None
    #----------------------------------------------  
    @property
    def key(self):
        return self._key
    #----------------------------------------------  
    @key.setter
    def key(self, key_var):
        if key_var is not None:
            print('setting key value')
            self._key = key_var
            self.make_fernet()
    #----------------------------------------------  
    def make_fernet(self):
        if self.key is not None and self.key != "":
            self.fernet = Fernet(self.key)
    #----------------------------------------------  
    def crypt_it(self, plainT:str):
        self.plainText = plainT.encode('utf-8')
        if self.key is not None and self.key != "" and self.fernet is not None:
            self.cipherText = self.fernet.encrypt(self.plainText)
            return self.cipherText.decode('utf-8')
    #----------------------------------------------  
    def decrypt_it(self, cipherT:str):
        self.cipherText = cipherT.encode('utf-8')
        if self.key is not None and self.key != "" and self.fernet is not None:
            self.plainText = self.fernet.decrypt(self.cipherText)
            return self.plainText.decode('utf-8')
    #----------------------------------------------  
    def generate_key(self):
        self._key = Fernet.generate_key()
        with open('keys.sys', 'wb') as keysFile:
            keysFile.write(self._key)

    #----------------------------------------------  
    def load_key(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, 'rb') as keyFile:
                self._key = keyFile.read()
                self.make_fernet()
    #----------------------------------------------  
    def batch_passcodes(self, input_csv:str):
        all_clients = []
        if os.path.exists(input_csv):
            with open(input_csv, 'r', newline='') as csv_file:
                csvreader = csv.reader(csv_file, delimiter=",")
                row_count = 0
                for row in csvreader:
                    if row_count > 0:
                        all_clients.append('-'.join(row))
                    row_count += 1

        for client in all_clients:
            self.generate_key()
            self.make_fernet()
            split_info = client.split('-')
            client_name = split_info[0]
            days_licensed = int(split_info[1])
            num_licenses = int(split_info[2])
            timeStamp = datetime.strftime(datetime.utcnow(), "%Y_%m_%d %H:%M:%S")
            dateStamp = datetime.strftime(datetime.utcnow(), "%Y_%m_%d")
            passcode_file = 'licensing/' + client_name + timeStamp + ".lic"
            with open(passcode_file, 'w') as license_opfile:
                license_opfile.write(f'Licenses generated for: {client_name}\n')
                license_opfile.write(f'Total number of licenses: {num_licenses}\n')
                license_opfile.write(f'Time of Generation: {timeStamp}\n')
                license_opfile.write(f'License duration: {days_licensed}\n')
                license_opfile.write(f'Encryption key: {self._key.decode()}\n')
                license_opfile.write(f'License Keys:\n')

                for l in range(0,num_licenses):
                    plainText = client + "-" + str(l+1)
                    cypherText = self.crypt_it(plainText)
                    license_opfile.write(f'"{cypherText}",\n')

#----------------------------------------------  
    def batch_codeGenerate(self, input_csv:str):
        all_clients = []
        try:
            if os.path.exists(input_csv):
                with open(input_csv, 'r', newline='') as csv_file:
                    csvreader = csv.reader(csv_file, delimiter=",")
                    row_count = 0
                    for row in csvreader:
                        if row_count > 0: #to avoid processing the header row
                            valid_till_date = datetime.now() +  timedelta( days = int(row[1]) )   
                            valid_till_str = datetime.strftime(valid_till_date, "%Y^%m^%d")
                            client_info = '-'.join(row) + '-' + valid_till_str
                            all_clients.append(client_info)
                        row_count += 1
        except Exception as e:
            print(f'Unable to create client list-{self.__class__}--batchCodeGenerate--{str(e)}')

        try:    
            for client in all_clients:
                self.generate_key()
                self.make_fernet()
                split_info = client.split('-')
                client_name = split_info[0]
                days_licensed = int(split_info[1])
                num_licenses = int(split_info[2])
                valid_till = split_info[3]
                feret_key_str = self._key.decode('utf-8')
                timeStamp = datetime.strftime(datetime.utcnow(), "%Y_%m_%d %H:%M:%S")
                dateStamp = datetime.strftime(datetime.utcnow(), "%Y_%m_%d")
                passcode_file = client_name + timeStamp + ".csv"
                with open(passcode_file, 'w') as license_opfile:
                    license_opfile.write("client,crypto_key,license_key,key_num,valid_period,valid_till\n") #header of the generated license file

                    # license_opfile.write(f'Licenses generated for: {client_name}\n')
                    # license_opfile.write(f'Total number of licenses: {num_licenses}\n')
                    # license_opfile.write(f'Time of Generation: {timeStamp}\n')
                    # license_opfile.write(f'License duration: {days_licensed}\n')
                    # license_opfile.write(f'Encryption key: {self._key.decode()}\n')
                    # license_opfile.write(f'License Keys:\n')

                    for l in range(0,num_licenses):
                        plainText = client + "-" + str(l+1)
                        print(plainText)
                        cypherText = self.crypt_it(plainText)
                        license_opfile.write(f'{client_name},{feret_key_str},{cypherText},{str(l+1)},{str(days_licensed)},{valid_till}\n')
        except Exception as e:
            print(f'unable to generate client keys-{self.__class__}--batchCodeGenerate--{str(e)}')

#------------------------end of class -------------------------
k1 = keyGen()
k1.batch_codeGenerate(input_csv="passcode_input.csv")