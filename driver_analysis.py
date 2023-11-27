import pandas as pd
from pandasql import sqldf

drivers = pd.read_csv(r'drivers.csv')
results = pd.read_csv(r'results.csv')

#%%
results = results[results['positionOrder']==1]
#%%
results = results.groupby(results['driverId'])['positionOrder'].sum()
#%%
drivers['fullname']=drivers['forename']+' '+drivers['surname']
#%%
df = pd.merge(drivers,results, on='driverId', how='left')
#%%
#df.head()
#%%
column_list=['driverId','fullname','positionOrder']
final_data = df[column_list]
#%%
final_data=final_data.rename(columns={'positionOrder':'Total Wins'})
#%%
final_data['Total Wins']=final_data['Total Wins'].fillna(0)
#%%
final_data['Total Wins']=final_data['Total Wins'].astype(int)
#%%
#final_data.columns
#%%
print("""THE LIST IS ONLY DRIVERS WHO HAVE WON (COME 1ST) IN AT LEAST ONE RACE. IF A DRIVER HAS NOT WON 
ANY RACE YET, THEIR NAME WON'T BE ON THE LIST.""")
print("Here is the list of the top 20 drivers with the highest amount of race wins\n")

query = ("""select fullname as `Full Name`, `Total Wins` from final_data where `Total Wins`>20 order by 
         `Total Wins` DESC;""")
qresult = sqldf(query, globals())
print(qresult)

while True:
    found = False
    name = input("Enter The name you want to search for! \n")
    for index, row in final_data.iterrows():
        if name.lower() == row['fullname'].lower():
            first_name, second_name = name.split()
            first_name=first_name.capitalize()
            second_name=second_name.capitalize()
            fullname = first_name+' '+second_name
            print(f"{fullname} has won {row['Total Wins']}.")
            found = True
            break
    if not found:
        print("Not in List")


