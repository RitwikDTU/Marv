import requests
import datetime as dt
import hashlib
import pandas as pd
from pprint import pprint as pp

'''Class containing get_dataframe() function to fetch Marvel characters data and transform all the data into a dataframe.'''

class Marvel():

    def __init__(self, public_key = None, private_key = None, timestamp = dt.datetime.now().strftime('%Y-%m-%d%H:%M:%S')):

        if public_key is None or (private_key is None or (public_key == '' or private_key == '')):
            raise Exception('Public key / Private key missing !')
        
        else:
            self.public_key = public_key
            self.private_key = private_key
            self.timestamp = timestamp


    def hash_generator(self):

        public_key = self.public_key
        private_key = self.private_key
        timestamp = self.timestamp

        hash_md5 = hashlib.md5()
        hash_md5.update(f'{timestamp}{private_key}{public_key}'.encode('utf-8'))
        hashed_params = hash_md5.hexdigest()

        self.hash = hashed_params


    '''get_dataframe() function used to fetch character data from Marvel website'''

    def get_dataframe(self,nameStartsWith = None):

        self.hash_generator() # Generating Hash using the keys

        character_data_list =[]
        
        if nameStartsWith is None or nameStartsWith == '':

            for i in range(16): # 16 iterations for fetching all the 1562 marvel characters (100 characters in each iteration)

                params = {'ts':self.timestamp, 'apikey':self.public_key, 'hash':self.hash,'limit':100, 'offset':100*i}
                response = requests.get('https://gateway.marvel.com:443/v1/public/characters',params)

                result = response.json()

                # Taking a copy of the result json file
                result_copy = result

                # Extracting characters' information from the json object and storing them into a list 

                for j in range(len(result_copy['data']['results'])):
                    l = []
                    l.append(result_copy['data']['results'][j]['id'])
                    l.append(result_copy['data']['results'][j]['name'])
                    l.append(result_copy['data']['results'][j]['events']['available'])
                    l.append(result_copy['data']['results'][j]['series']['available'])
                    l.append(result_copy['data']['results'][j]['comics']['available'])
                    l.append(result_copy['data']['results'][j]['stories']['available'])

                    character_data_list.append(l) # List containing all characters' information

                print('Fetched ',100*(i+1), 'characters')
            

            # Converting list to final dataframe
            character_dataframe = pd.DataFrame.from_records(character_data_list)
            character_dataframe.rename(columns = {0:'Character Id',1:'Name',2:'Event Appearances',3:'Series Appearances',4:'Comics Appearances',5:'Stories Appearances'}, inplace = True)
            character_dataframe.set_index('Character Id',inplace=True)

        else:
            params = {'ts':self.timestamp, 'apikey':self.public_key, 'hash':self.hash,'limit':100, 'nameStartsWith':nameStartsWith}
            response = requests.get('https://gateway.marvel.com:443/v1/public/characters',params)

            result = response.json()

            # Taking a copy of the result json file
            result_copy = result

            # Extracting characters' information from the json object and storing them into a list 

            for j in range(len(result_copy['data']['results'])):
                l = []
                l.append(result_copy['data']['results'][j]['id'])
                l.append(result_copy['data']['results'][j]['name'])
                l.append(result_copy['data']['results'][j]['events']['available'])
                l.append(result_copy['data']['results'][j]['series']['available'])
                l.append(result_copy['data']['results'][j]['comics']['available'])
                l.append(result_copy['data']['results'][j]['stories']['available'])

                character_data_list.append(l) # List containing all characters' information

            print('Fetching completed !')
        

            # Converting list to final dataframe
            character_dataframe = pd.DataFrame.from_records(character_data_list)
            character_dataframe.rename(columns = {0:'Character Id',1:'Name',2:'Event Appearances',3:'Series Appearances',4:'Comics Appearances',5:'Stories Appearances'}, inplace = True)
            character_dataframe.set_index('Character Id',inplace=True)



        self.df = character_dataframe

        return character_dataframe

# These commands will execute when marvel_api.py is run using CLI

def main():
    pub_key = input('Enter Public key(API Key)')
    priv_key = input('Enter private key (Hash key)')
    nameStart = input('Enter preferred starting letter of character name ( Leave empty to fetch all characters )')
    marvel = Marvel(pub_key,priv_key)
    character_df = marvel.get_dataframe(nameStart)
    print(character_df)

if __name__ == "__main__":
    main()
        




        


    