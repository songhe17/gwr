# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 01:45:39 2020

@author: g
"""

#2/15 - 5/25
import pandas as pd
import time
from tqdm import tqdm
import json
import pickle
import matplotlib.pyplot as plt

dates_2_5 = ['2020-02-15', '2020-02-16', '2020-02-17', '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24', '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29', '2020-03-30', '2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06', '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16', '2020-04-17', '2020-04-18', '2020-04-19', '2020-04-20', '2020-04-21', '2020-04-22', '2020-04-23', '2020-04-24', '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28', '2020-04-29', '2020-04-30', '2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08', '2020-05-09', '2020-05-10', '2020-05-11', '2020-05-12', '2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19', '2020-05-20', '2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25']
dump = False
if dump:
    path = 'google_mobility.csv'
    start = time.time()
    data = pd.read_csv(path)
    print(time.time() - start)
    # =============================================================================
    # path = 'Global_Mobility_Report.csv'
    # data = pd.read_csv(path)
    # print(data.keys())
    # =============================================================================
    print(type(data))
    print(data['Region Type'][0])
    #print(data.iloc[20])
    data_len = len(data['Region Type'])
    data_dict = {}
    iloc = data.iloc
    for i in tqdm(range(data_len)):
        i = data_len - i - 1
        country = iloc[i]['Country']
        state = iloc[i]['State/Province']
        county = iloc[i]['County']
        change = iloc[i]['Percent Change']
        date = iloc[i]['Date']
        date = date.replace('-', '/')
        if i != data_len - 1 and iloc[i+1]['Country'] == 'United States' and country != 'United States':
            break
        if country == 'United States':
            key = tuple([country, state, county])
            
            if key not in data_dict:
                data_dict[key] = []
            data_dict[key].append([change,date])
        
    
    
    save_path = 'gb.pkl'
    with open(save_path, 'wb') as f:
        pickle.dump(data_dict, f)
    

file = 'gb.pkl'
with open(file, 'rb') as f:
    data = pickle.load(f)
    #print(list(data.keys()))

ala = data[('United States', 'Alabama', 'Lauderdale County')]
print(all(ele[0] != ele[0] for ele in ala))
    
# =============================================================================
# data_state = {}
# for i, (key, value) in enumerate(data.items()):
#     conti = False
#     for ele in value:
#         if ele != ele:
#             conti = True
#     if conti:
#         continue
#     if key[1] not in data_state:
#         data_state[key[1]] = []
#     data_state[key[1]].append(value)
# =============================================================================
cal_data = {}
k = 0
#print(data[('United States', 'Alaska', 'North Slope')])
for key, value in data.items():

    if key[1] != 'California':
        continue
    if key[2] != key[2]:
        continue
    if all(ele[0] != ele[0] for ele in value):
        continue
    for i in range(len(value)):
# =============================================================================
#         if i == 0 or i == len(value) - 1 and value[i][0] != value[i][0]:
#             value[i][0] = 0.0
#         elif value[i][0] != value[i][0]:
#             if value[i-1][0] != value[i-1][0] and value[i+1][0] == value[i+1][0]:
#                 value[i][0] = value[i+1][0]
#             elif value[i-1][0] == value[i-1][0] and value[i+1][0] != value[i+1][0]:
#                 value[i][0] = value[i-1][0]
#             else:
#                 
#                 value[i][0] = (value[i-1][0] + value[i+1][0]) / 2
#         if value[i][0] == 0:
#             k+=1
# =============================================================================
        if value[i][0] != value[i][0]:
            continue
        cal_data[(key[2], value[i][1])] = value[i][0]
print(k, len(cal_data))

#print(cal_data)
for i,j in cal_data.keys():
    if i != i:
        print(j)
with open('cal_flow_data.pkl','wb') as f:
    pickle.dump(cal_data,f)
# =============================================================================
#         cal_data[key[2]]['cases'] = []
#         cal_data[key[2]]['deaths'] = []
#         cal_data[key[2]]['date'] = []
# =============================================================================
#print(cal_data.keys())
    #plt.figure(i)
    #plt.plot(value)
#print(cal_data['Modoc County']['flow'])

# =============================================================================
# path = 'covid-19-data/us-counties.csv'
# start = time.time()
# data = pd.read_csv(path)
# print(time.time() - start)
# iloc = data.iloc
# print(iloc[0])
# print(iloc[1])
# print(iloc[2])
# old_county = ''
# for ele in iloc:
#     if ele['state'] != 'California':
#         continue
#     date = ele['date']
#     county = ele['county'] + ' County'
#     if county not in cal_data:
#         continue
#     cases = ele['cases']
#     deaths = ele['deaths']
#     
#     float_date = float(date.split('-')[1][1] + '.' + date.split('-')[2])
#     if float_date < 2.15 or float_date > 5.25:
#         continue  
# =============================================================================

# =============================================================================
#     cal_data[county]['cases'].append(float(cases))
#     cal_data[county]['deaths'].append(float(deaths))
#     cal_data[county]['date'].append(date)
# 
# for key,value in cal_data.items():
#     if len(value['date']) == 0:
#         continue
#     index = dates_2_5.index(value['date'][0])
#     attr = [float('NaN')] * index
#     value['date'] = dates_2_5[:index] + value['date']
#     value['deaths'] = attr + value['deaths']
#     value['cases'] = attr + value['cases']
# =============================================================================
# =============================================================================
# print(cal_data)
# file_name = 'cal_data.json'    
# with open(file_name, 'w') as f:
#     json.dump(cal_data, f)
# =============================================================================

        
    