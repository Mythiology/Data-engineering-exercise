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






# we need
# Restaurant Id, get by using {'restaurant': {'R': {'res_id': 18537536}
# Restaurant Name {'restaurant': {name': "Chili's Grill & Bar"
# Country {res: {location:{country_id:}}}
# City {res: {location:{city_id:}}}
# User Rating Votes {res: {user_rating:{votes:}}
# User Aggregate Rating (as a float) {res: {user_rating:{'aggregate_rating':}}
# Cuisines {res: {'R':{cuisines:}}
# Event Data Extraction {res: {zomato_events:}}

# "restaurants": [{"restaurant": {"R": {"res_id": 18649486}, "apikey": "cba15beb4c265876a9828f242b4cf41c", "id": "18649486", "name": "The Drunken Botanist", "url": "https://www.zomato.com/ncr/the-drunken-botanist-dlf-cyber-city-gurgaon?utm_source=api_basic_user&utm_medium=api&utm_campaign=v2.1", "location": {"address": "Unit 1B & 1C, Upper Ground Floor-C, Building 10C, Cyber Hub, DLF Cyber City, Gurgaon", "locality": "Cyber Hub, DLF Cyber City", "city": "Gurgaon", "city_id": 1, "latitude": "28.4936741035", "longitude": "77.0883342996", "zipcode": "", "country_id": 1, "locality_verbose": "Cyber Hub, DLF Cyber City, Gurgaon"}, "switch_to_order_menu": 0, "cuisines": "Continental, Italian, North Indian, Chinese", "average_cost_for_two": 1500, "price_range": 3, "currency": "Rs.", "offers": [], "zomato_events": [{"event": {"event_id": 322331, "friendly_start_date": "06 March", "friendly_end_date": "28 August", "friendly_timing_str": "Wednesday, 6th March - Wednesday, 28th August", "start_date": "2019-03-06", "end_date": "2019-08-28", "end_time": "23:59:59", "start_time": "20:00:00", "is_active": 1, "date_added": "2019-03-06 11:41:21", "photos": [{"photo": {"url": "https://b.zmtcdn.com/data/zomato_events/photos/5a1/ac34cf3c271c9052e9d248c243df65a1_1551852711.jpg", "thumb_url": "https://b.zmtcdn.com/data/zomato_events/photos/5a1/ac34cf3c271c9052e9d248c243df65a1_1551852711.jpg?fit=around%7C100%3A100&crop=100%3A100%3B%2A%2C%2A", "order": 0, "md5sum": "ac34cf3c271c9052e9d248c243df65a1", "id": 434436, "photo_id": 434436, "uuid": 52695233531, "type": "FEATURED"}}], "restaurants": [], "is_valid": 1, "share_url": "http://www.zoma.to/r/0", "show_share_url": 0, "title": "BackToBasic Wednesdays !!\n\n\n", "description": "https://www.facebook.com/events/347477306085841/?ti=cl\n\nThe twilight and timbre, the delicious drinks and vibrant crowd. Are you ready to make Wednesdays awesome again with Rock Nights & sensational new Bands every week? Then you know where to find me! \n\nAlways High, Always Rocking only at TDB.", "display_time": "08:00 pm onwards", "display_date": "06 March - 28 August", "is_end_time_set": 0, "disclaimer": "Restaurants are solely responsible for the service; availability and quality of the events including all or any cancellations/ modifications/ complaints.", "event_category": 1, "event_category_name": "", "book_link": "", "types": [], "share_data": {"should_show": 0}}}]


#[{'photo': {'url': 'https://b.zmtcdn.com/data/zomato_events/photos/847/acb0693c612ec13c15e618d4bf3cf847_1507619388.jpg', 'thumb_url': 'https://b.zmtcdn.com/data/zomato_events/photos/847/acb0693c612ec13c15e618d4bf3cf847_1507619388.jpg?fit=around%7C100%3A100&crop=100%3A100%3B%2A%2C%2A', 'order': 0, 'md5sum': 'acb0693c612ec13c15e618d4bf3cf847', 'id': 235171, 'photo_id': 235171, 'uuid': 1507619385639573, 'type': 'NORMAL'}}], 'restaurants': [], 'is_valid': 1, 'share_url': 'http://www.zoma.to/r/0', 'show_share_url': 0, 'title': 'Festive Food Bonanza || Special Buffet Prices starting @ Rs. 499 + || Full Day Alacarte', 'description': 'Come @ participate in the revelry at Jungle Jamboree Noida with humongous themes, giant animals, mystic Jungle, mesmerizing Aqua Zone, Machaan & much more. Savor the never ending 7 Course Buffet spread special pricing starting @ Rs. 499 + taxes and an all day Alacarte menu.!', 'display_time': '11:45 am - 11:00 pm', 'display_date': '21 January - 31 May', 'is_end_time_set': 1, 'disclaimer': 'Restaurants are solely responsible for the service; availability and quality of the events including all or any cancellations/ modifications/ complaints.', 'event_category': 0, 'event_category_name': '', 'book_link': '', 'types': [], 'share_data': {'should_show': 0}}}, {'event': {'event_id': 161417, 'friendly_start_date': '21 January', 'friendly_end_date': '31 May', 'friendly_timing_str': 'Monday, 21st January - Friday, 31st May', 'start_date': '2019-01-21', 'end_date': '2019-05-31', 'end_time': '18:00:00', 'start_time': '16:00:00', 'is_active': 1, 'date_added': '2017-10-10 12:58:05', 'photos': [{'photo': {'url': 'https://b.zmtcdn.com/data/zomato_events/photos/21a/7db6ab62451f0c3b57f0b17a42aaa21a_1552391084.jpg', 'thumb_url': 'https://b.zmtcdn.com/data/zomato_events/photos/21a/7db6ab62451f0c3b57f0b17a42aaa21a_1552391084.jpg?fit=around%7C100%3A100&crop=100%3A100%3B%2A%2C%2A', 'order': 0, 'md5sum': '7db6ab62451f0c3b57f0b17a42aaa21a', 'id': 438384, 'photo_id': 438384, 'uuid': 1552391018998755, 'type': 'NORMAL'}}