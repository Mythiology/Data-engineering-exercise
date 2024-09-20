import pandas as pd
import json
import csv
import logging

"""logging configuration"""
logging.basicConfig(
    filename = "Data Engineering.log",
    format = '%(asctime)s %(message)s',
    filemode='w'
)

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

"""reading Country-Code.xlsx"""
try:
    dataframe = pd.read_excel('datafiles/Country-Code.xlsx', usecols = [0])
    logger.info('[Status] Country-Code.xlsx has been read.')
except Exception as error:
    logger.error('[Error] Country-Code.xlsx file reading: {}'.format(error))

"""extracting dataframe to list"""
temp = dataframe.values.tolist()
country_codes = []
for ele in temp:
    country_codes.append(int(ele[0]))
logger.info('[Status] Dataframe has been extracted from Country-Code.xlsx.')

"""reading restaurant_data.json"""
try:
    f = open('datafiles/restaurant_data.json', 'r', encoding = 'utf-8')
    file = json.loads(f.read())
    logger.info('[Status] restaurant_data.json has been read.')
except Exception as error:
    logger.error('[Error] restaurant_data.json file reading: {}'.format(error))


"""normalising the nested json to have a cleaner data"""
data = pd.json_normalize(file, record_path="restaurants")
logger.info('[Status] restaurant_data.json file has been normalised.')

"""extracting data"""
restaurant_details = []
event_details = []
raw_ratings = []

for ele in range(len(data)):
    temp = {}
    if int(data['restaurant.location.country_id'][ele]) in country_codes:
        temp['Restaurant_id'] = int(data['restaurant.id'][ele])
        temp['Name'] = data['restaurant.name'][ele]
        temp['Country'] = int(data['restaurant.location.country_id'][ele])
        temp['City'] = int(data['restaurant.location.city_id'][ele])
        temp['Votes'] = int(data['restaurant.user_rating.votes'][ele])
        temp['Aggregate Rating'] = float(data['restaurant.user_rating.aggregate_rating'][ele])
        temp['Cuisines'] = data['restaurant.cuisines'][ele]

        """extracting user ratings"""
        raw_ratings.append([data['restaurant.user_rating.rating_text'][ele],
                            temp['Aggregate Rating']])
        raw = data['restaurant.zomato_events'][ele]
        
        """filtering out empty event values"""
        if isinstance(raw,list): 

            """Task did not specify what Event Data Extraction is so 
            we assume that we need to display all the info"""
            temp['Event_Data'] = raw 

            """extracting data from events"""
            for event in raw:
                row = {}

                """Assume that events starting and ending in April 2019 is what we need"""
                if '2019-04' in event['event']['start_date'] or '2019-04' in event['event']['end_date']:
                    """assume that every photo is needed"""
                    row['Event_id'] = int(event['event']['event_id'])
                    row['Restaurant_id'] = int(data['restaurant.id'][ele])
                    row['Name'] = data['restaurant.name'][ele]
                    row['Photo_Url'] = event['event']['photos'] 
                    row['Event_Title'] = event['event']['title']                   
                    row['Start_Date'] = event['event']['start_date']
                    row['End_Date'] = event['event']['end_date']
                    event_details.append(row)
        else:
            temp['Event_Data'] = 'NA'
        restaurant_details.append(temp)
# print(restaurant_details)
logger.info('[Status] Restaurant data has been extracted.')

"""need to write utf-8 for special characters like पुणे """
with open('results/restaurant_details.csv', 'w', encoding = 'utf-8') as file: 
    header = ['Restaurant_id', 'Name', 'Country', 'City',
              'Votes', 'Aggregate Rating', 'Cuisines', 'Event_Data']
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()
    try:
        for ele in restaurant_details:
            writer.writerow(ele)
        logger.info('[Status] restaurant_details.csv has been written.')
    except Exception as error:
        logger.error('[Error] restaurant_details.csv file writing: {}'.format(error))

"""cleaning up photo urls, since there can be multiple photos for one event,
assumed that all main photos (not including thumbnail photos) are needed"""
for ind in range(len(event_details)):
    pics = ""
    for ele in event_details[ind]['Photo_Url']:
        pics += (ele['photo']['url']) + ','
    
    if len(pics) == 0:
        event_details[ind]['Photo_Url'] = 'NA' 
    else:
        event_details[ind]['Photo_Url'] = pics.strip()
# print(event_details)
logger.info('[Status] Event data has been extracted.')

with open('results/restaurant_events.csv', 'w', encoding = 'utf-8') as file: 
    header = ['Event_id', 'Restaurant_id', 'Name', 'Photo_Url',
              'Event_Title', 'Start_Date', 'End_Date']
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()
    try:
        for ele in event_details:
            writer.writerow(ele)
        logger.info('[Status] restaurant_events.csv has been written.')
    except Exception as error:
        logger.error('[Error] restaurant_events.csv file writing: {}'.format(error))

"""filtering out ratings"""
ratings = [['Excellent',[5,0]],['Very Good',[5,0]],
           ['Good',[5, 0]],['Average',[5,0]],
           ['Poor',[5, 0]]]

for row in raw_ratings:
    for ele in ratings:
        if row[0] == ele[0]:
            if ele[-1][0] > row[-1] and ele[-1][-1] != 0:
                ele[-1][0] = row[-1]
            elif ele[-1][-1] <= row[-1]:
                ele[-1][-1] = row[-1]

"""filtering out default values"""
for row in ratings:
    if ele[-1][0] == 5:
        ele[-1][0] = 0
    elif ele[-1][-1] == 0:
        ele[-1][-1] = 5
logger.info('[Status] User rating has been extracted.')

# print(ratings)
"""Output:
[['Excellent', [4.5, 4.9]], ['Very Good', [4.0, 4.4]], ['Good', [3.5, 3.9]], ['Average', [2.5, 3.4]], ['Poor', [0, 2.2]]]
Here we can tell that the range of poor is 0 ~ 2.2, average is 2.5 ~ 3.4, good is 3.5 ~ 3.9, 
very good is 4.0 ~ 4.4, excellent is 4.5 ~ 4.9. 
"""

