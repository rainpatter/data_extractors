import pandas as pd

df = pd.read_csv('application_ids.csv')

print(df)

def convert(id):
    try:
        if (id.startswith('STD') or id.startswith('LTD')) and int(id[4:]) < 1000:
            return 'NA/'+str(id[4:])
        else:
            return id
    except:
        return id

id_list = df['Application ID'].tolist()
df['Updated Application ID'] = df['Application ID'].apply(
    lambda x: convert(x)
)


print(df)

df.to_csv('master_id_list.csv', header=True)

# print(id_list)

# new_list = []
# for id in id_list:
#     try:
#         if (id.startswith('STD') or id.startswith('LTD')) and int(id[4:]) < 1000:
#             new_id = 'NA/'+str(id[4:])
#             new_list.append(new_id)
#         else:
#             new_list.append(id)
#     except:
#         new_list.append(id)
# print(new_list)