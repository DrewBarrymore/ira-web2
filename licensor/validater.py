from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os
import uuid
import requests

class license_checker:
    """Takes license key and decodes, checks with a list of keys using encryption key"""

    textKey = "w9a23CIW8jouV6w8fGNd2mG_nDMAj69XnPWwR3TE9Sg=" #local encryption decryption key
    checker_url = 'http://127.0.0.1:8000/licensor/installation_check/'
    checker_payload = {
        'lic_key' : None,
        'mac_id' : None
    }
    
    valid_till = None
    #------------------------------------------------------------------------------------------------
    def __init__(self, feret_key:str=textKey, p_code:str=None,) -> None:
        self._key = feret_key.encode('utf-8')
        self.fernet = Fernet(self._key)
        self.passCode = p_code
        self.verified = False
    #------------------------------------------------------------------------------------------------
    # def verify_licKey(self,codeText):
    #     """TBI central database checking license used or not"""
    #     if codeText is not None and codeText !="":
    #         if codeText in self.passCodes:
    #             self.passCode = codeText
    #             self.verified = True
    #             return True
    #     return False
    #------------------------------------------------------------------------------------------------
    def save_licKey(self):
        if self.passCode is not None and self.passCode != "" and self.verified == True:
            with open("ira.lic", 'wb') as lic_file:
                lic_file.write(self.passCode.encode('utf-8'))
                lic_file.write('\n'.encode('utf-8'))
                lic_file.write(datetime.strftime(datetime.utcnow(), "%Y_%m_%d").encode('utf-8'))
    #------------------------------------------------------------------------------------------------
    def save_localKey(self):
        '''
        Saves Encrypted local information for software to read on every startup
        '''
        # if self.passCode is not None and self.passCode != "" and self.verified == True:
        #find current working directory
        if self.valid_till is not None:
            with open("ira.lic", 'w+b') as lic_file:
                self.this_node = str( uuid.getnode() )
                if self.this_node is None:
                    self.this_node = "unkown"
                self.local_str_b = (self.this_node+ '-' +self.valid_till).encode('utf-8')
                self.local_crypto = self.fernet.encrypt(self.local_str_b)
                lic_file.write(self.local_crypto)
    #------------------------------------------------------------------------------------------------
    def read_licInfo(self):
        if os.path.exists("ira.lic"):
            with open('ira.lic', 'rb') as lic_file:
                self.passCode = lic_file.readline()
                self.passCode_str = self.passCode.decode('utf-8')
                license_date_str = lic_file.readline().strip().decode('utf-8')
                self.license_date = datetime.strptime(license_date_str, "%Y_%m_%d")
                self.lic_info = Fernet.decrypt(self.fernet, self.passCode).decode('utf-8')
                self.lic_components = self.lic_info.split('-')
                self.lic_dict = {
                    "User" : self.lic_components[0],
                    "days_licensed" : int(self.lic_components[1]),
                    "start_date" : self.license_date
                }

                self.time_left = self.lic_dict["start_date"] + timedelta(days=self.lic_dict['days_licensed']) - datetime.utcnow()
                # print(self.time_left.days)
    #------------------------------------------------------------------------------------------------
    def read_passcode(self):
        if self.passCode is not None:
            try:
                self.lic_info = Fernet.decrypt(self.fernet, self.passCode).decode('utf-8')
                self.lic_components = self.lic_info.split('-')
                self.lic_dict = {
                    "User" : self.lic_components[0],
                    "days_licensed" : int(self.lic_components[1]),
                    "license_lotSize" : int(self.lic_components[2]),
                    "valid_till" : str(self.lic_components[3]),
                    "key_sequence" : int(self.lic_components[4]),
                    "valid_till_date": datetime.strptime(str(self.lic_components[3]), "%Y^%m^%d")
                    # "start_date" : self.license_date
                }
                return self.lic_dict
            except Exception as e:
                print(f'Unable to decode passkey-{self.__class__}--readPasscode--{str(e)}')
    #------------------------------------------------------------------------------------------------
    def read_localKey(self):
        if os.path.exists("ira.lic"):
            try:
                with open("ira.lic", 'r+b') as lic_file:
                    localKey = lic_file.read()
                local_info = self.fernet.decrypt(localKey).decode('utf-8')
                info_breakup = local_info.split('-')
                local_infoDict = {
                    'mac_id':info_breakup[0],
                    'validity_str' : info_breakup[1],
                    'validity_date' : datetime.strptime(info_breakup[1], '%Y^%m^%d'),
                    'validity_time' : int((datetime.strptime(info_breakup[1], '%Y^%m^%d') - datetime.now()).days)
                }
                return local_infoDict
            except Exception as e:
                print(f'Unable to find license information--{self.__class__}--readLocalKey--{str(e)}')
                return 1
        else:
            return 1
    #------------------------------------------------------------------------------------------------
    def preInstall_check(self):
        '''
        Client side function - to send preInstall request to server
        '''
        try:
            if self.passCode is not None:
                self.checker_payload['lic_key'] = self.passCode
                self.checker_payload['mac_id'] = uuid.getnode()
                outcome = requests.get(url=self.checker_url, params=self.checker_payload)
                response_info = outcome.text.split('-')
                status = response_info[0]
                if status == 'OK':
                    self.valid_till = response_info[1]
                    self.save_localKey()
                    return 0
                else:
                    return 1
            else:
                print('PassCode not properly provided')
                return 1
            
        except Exception as e:
            print(f'Unable to perform preinstall check-{self.__class__}--PreInstallCheck--{str(e)}')
            return 1
    #------------------------------------------------------------------------------------------------
    def postInstall_check(self):
        try:
            local_readings = self.read_localKey()
        except Exception as e:
            print(f'Unable to readLocalKey--{self.__class__}--postInstallCheck--{str(e)}')
            return 1 #there is an error in trying to read local key
        if local_readings is not None:
            if (local_readings['mac_id'] == str( uuid.getnode() )) and local_readings['validity_time'] > 0:
                return 0 #all is well
            else:
                return 2 # readings are there but not okay
        else:
            return 3 #readings are not there
        
#------------------------end of class -------------------------

# li = license_checker(p_code='gAAAAABkD14RezD9l_g02Fz53X3HNoecwE_EVOtBjKyAvEpxnmfM5j3eo7DyKvqC-ehLV6C4K5GtMAopLvcj_AXemv8TSv1M425Cx_hW5vHnbA4HqGhBZQTUMS1LBreoFzK-0YiSf1Jv')
# print( li.postInstall_check() )
