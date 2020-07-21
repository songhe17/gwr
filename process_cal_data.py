   # -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 00:16:55 2020

@author: g
"""


import pandas as pd
import json
import pickle
import numpy as np

dates_2_5 = ['2020-02-15', '2020-02-16', '2020-02-17', '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24', '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29', '2020-03-30', '2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06', '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16', '2020-04-17', '2020-04-18', '2020-04-19', '2020-04-20', '2020-04-21', '2020-04-22', '2020-04-23', '2020-04-24', '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28', '2020-04-29', '2020-04-30', '2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08', '2020-05-09', '2020-05-10', '2020-05-11', '2020-05-12', '2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19', '2020-05-20', '2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25']
all_dates = [date.replace('-', '/') for date in dates_2_5]
week_day = [(i+5) % 7 for i in range(len(all_dates))]
#print(week_day)

reg_data = pd.read_csv('selected_data_norm.csv')

flow_data = pickle.load(open('cal_flow_data.pkl','rb'))

k = list(reg_data.keys())

print(k)
    
# =============================================================================
# reg_keys = ['total_population', 'area_sqmi', 'percent_smokers',
#             'percent_adults_with_obesity', 'food_environment_index', 'percent_physically_inactive',
#             'percent_with_access_to_exercise_opportunities', 'percent_excessive_drinking',
#             'chlamydia_rate', 'mental_health_provider_rate', 'high_school_graduation_rate',
#             'percent_some_college', 'violent_crime_rate', 'average_daily_pm2_5',
#             'overcrowding', 'percent_drive_alone_to_work', 'life_expectancy', 'percent_65_and_over',
#             'percent_below_poverty']
# =============================================================================
#TODO
reg_keys = ['total_population', 'area_sqmi', 'population_density_per_sqmi',
            'percent_smokers', 'percent_adults_with_obesity',
            'percent_excessive_drinking', 'percent_uninsured',
            'percent_unemployed_CHR',
            'violent_crime_rate','life_expectancy',
            'percent_65_and_over', 'per_capita_income', 'percent_below_poverty']


info_keys = ['date', 'county', 'lat', 'lon', 'area_sqmi']
# date * county, check who is missing


county_dict = {}
available_dc = {}
counties = []
for ele in reg_data.iloc:
    date = '2020/0'+ele['date'][:4]
    if date[-1] == '/':
        date = date[:8] + '0' + date[-2]
    available_dc[(ele['county'], date)] = [ele['deaths'], ele['cases']]
    key = ele['county'] + ' County'
    if key not in county_dict:
        counties.append(ele['county'])
        county_dict[key] = {} 
        county_dict[key]['reg'] = [ele[factor] for factor in reg_keys]
        county_dict[key]['basic'] = {info: ele[info] for info in info_keys[1:]}

date_county_keys = []
for county in counties:
    for date in all_dates:
        date_county_keys.append((county, date))

covid_info = {}
k = 0
for dc in date_county_keys:
    covid_info[dc] = {}
    if dc not in available_dc:
        
        covid_info[dc]['death'] = 0
        covid_info[dc]['case'] = 0
    else:
        k += 1
        covid_info[dc]['death'] = available_dc[dc][0]
        covid_info[dc]['case'] = available_dc[dc][1]
#covid_info = {('2','4'): 5}
edited_covid_info = {}

for key, value in covid_info.items():
    county = key[0] + ' County'
    new_key = (county, key[1])
    edited_covid_info[new_key] = value
    
# =============================================================================
# print(list(county_dict.items())[0], '\n' * 4)
# print(list(edited_covid_info.items())[:10], '\n' * 4)
# print(list(flow_data.items())[:10], '\n' * 4)
# ====================================                                                 =========================================
save = {'y':[], 'x':[], 'latlon':[]}
for i, (key, value) in enumerate(edited_covid_info.items()):
    if key not in flow_data:
        continue
                                                  
    if int(key[1][6]) < 4:
        continue
    death = float(edited_covid_info[key]['death'])
    case = float(edited_covid_info[key]['case'])
    wd = week_day[all_dates.index(key[1])]
    if wd != 5:
        continue
    one_hot_wd = [0.0] * 7
    one_hot_wd[wd] = 1.0
    county_info = county_dict[key[0]]

    reg_info = [key for key in county_info['reg']]
    latlon = [np.random.normal(county_info['basic']['lat'], 0.1, 1)[0], np.random.normal(county_info['basic']['lon'], 0.1, 1)[0]]
    
    #county_info = [county_info[key] for key in county_info.keys()]
    #x = reg_info + one_hot_wd
    x = reg_info + [case]
    save['y'].append(flow_data[key])
    save['x'].append(x)
    save['latlon'].append(latlon)

# =============================================================================
# for key, value in save.items():
#     print(np.shape(value))
#     print(any(ele != ele for ele in value))
# =============================================================================
with open('data.json', 'w') as f:
    json.dump(save, f)

#print(save['y'])

#print(available_dc.keys())
# =============================================================================
# print(date_county_keys[:10])
# print(('Orange', '2020/02/15') in available_dc)
# print(available_dc)
# =============================================================================
# =============================================================================
# for i in available_dc:
#     if 'Orange' in i:
#         print(i)
# for i in date_county_keys:
#     if 'Orange' in i:
#         print(i)
#         break
# =============================================================================
#print(reg_dict.values())