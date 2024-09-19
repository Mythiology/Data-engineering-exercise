import pandas as pd
import csv

"""read 1st sheet of an excel file"""
dataframe = pd.read_excel('datafiles/Country-Code.xlsx', usecols = [0])

"""extracting dataframe to list"""
temp = dataframe.values.tolist()
country_codes = []
for ele in temp:
    country_codes.append(ele[0])

"""reading json file"""
data = pd.read_json('datafiles/restaurant_data.json')
temp2 = data.to_dict()
# print(len(temp2["restaurants"][0]))

restaurant_details = []

# print(temp2["restaurants"][0])
"""iterating through each serial number at the start"""
for ind in temp2["restaurants"].keys(): 
    """iterating through each restaurant data of each serial number"""
    for ele in temp2["restaurants"][ind]:
        temp = {}
        """checking if country code exists inside Country-code.xlsx"""
        if ele["restaurant"]['location']['country_id'] in country_codes:
            """extracting all the data"""
            temp['Restaurant_id'] = ele['restaurant']['R']['res_id']
            temp['Name'] = ele['restaurant']['name']
            temp['Country'] = ele['restaurant']['location']['country_id']
            temp['City'] = ele['restaurant']['location']['city_id']
            temp['Votes'] = ele['restaurant']['user_rating']['votes']
            temp['Aggregate Rating'] = float(ele['restaurant']['user_rating']['aggregate_rating'])
            temp['Cuisines'] = ele['restaurant']['cuisines']

            """assuming that all event data is needed since task never specify"""
            if "zomato_events" in ele['restaurant'].keys():
                temp['Event_Data'] = ele['restaurant']['zomato_events']
            else:
                temp['Event_Data'] = 'NA'
            restaurant_details.append(temp)

# setting up file writing
"""need to write utf-8 for special characters like पुणे """
with open('restaurant_details.csv', 'w', encoding = 'utf-8') as file: 
    header = ['Restaurant_id', 'Name', 'Country', 'City','Votes', 'Aggregate Rating', 'Cuisines', 'Event_Data']
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()
    for ele in restaurant_details:
        writer.writerow(ele)


event_details = []
for row in restaurant_details:
    details = row['Event_Data'] 
    temp = {}

    if details != 'NA':
        """might have multiple events for the same restaurant"""
        for ele in details:
            """we need to check if event hapens in April 2019"""
            if '2019-04' in ele['event']['start_date'] or '2019-04' in ele['event']['end_date']: 
                temp['Event_id'] = ele['event']['event_id']
                temp['Restaurant_id'] = row['Restaurant_id']
                temp['Name'] = row['Name']

                """might have more than one photo or no photos at all"""
                if len(ele['event']['photos']) == 0:
                    temp['Photo_Url'] = 'NA'
                else:
                    pic_url = []
                    for pic in ele['event']['photos']:
                        pic_url.append(pic['photo']['url'])
                    
                temp['Event_Title'] =  ele['event']['title']
                temp['Start_Date'] =  ele['event']['start_date']
                temp['End_Date'] =  ele['event']['end_date']
                event_details.append(temp)

# setting up file writing
with open('restaurant_events.csv', 'w', encoding = 'utf-8') as file: # need to write utf-8 for special characters like पुणे 
    header = ['Event_id', 'Restaurant_id', 'Name', 'Photo_Url','Event_Title', 'Start_Date', 'End_Date']
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()
    for ele in event_details:
        writer.writerow(ele)

