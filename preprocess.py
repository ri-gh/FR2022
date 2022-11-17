#pip install openpyxl
import pandas as pd
import requests

#we load the dataset for url

url='https://www.data.gouv.fr/fr/datasets/r/98eb9dab-f328-4dee-ac08-ac17211357a8'
r = requests.get(url)
open('temp.xls', 'wb').write(r.content)
df = pd.read_excel('temp.xls')


#we rename the columns named "Unamed"
for i in range (0,12):
    i= i*7
    df = df.rename(columns = {df.columns[i+21] :"N°Panneau",
                                            df.columns[i+22] :"Sexe",
                                            df.columns[i+23] :"Nom",
                                            df.columns[i+24] :"Prénom",
                                            df.columns[i+25] :"Voix",
                                            df.columns[i+26] :"% Voix/Ins",
                                            df.columns[i+27] :"% Voix/Exp" })

 #we create a list to have the index number of the first 20 columns that we'll keep (they are the same for every candidate) and add the seven next for each candidate
index_lst = list(range(0,20+1))

#We create a list to cut the 28 first columns of the df and append under the next +i  , 11 times
list_index = []
for i in range (0,12):
    i = i*7 # 84 rows divided by 12 candidates = 7 
    list_col= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,i+21, i+22 ,i+23,i+24,i+25,i+26,i+27]
    list_index.append(list_col)

#we append the columns as line under each 28 first columns 11 times (12 candidates)
df_global = pd.DataFrame()
for i in range (0,12):
    df_global = df_global.append(df.iloc[:,list_index[i]])

#we keep only the below named columns:
df_global =  df_global[['Code du département', 'Libellé du département',
       'Libellé de la commune','Nom','Voix', '% Abs/Ins', '% Blancs/Vot', '% Nuls/Vot',
       '% Exp/Vot', '% Voix/Ins', '% Voix/Exp']]

#we save the df as .csv file in our local directory
df_global.to_csv((r'your_local_path'), index = False, header=True)