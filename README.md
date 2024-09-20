# Data-engineering-exercise

## Installation of modules
Steps:
1) Run `pip install requirements.txt`
2) Run the python file `main.py`

## Short summary on how to design/deploy using cloud services and any decisions you made when designing solution
I would deploy this code by establishing an `SSH connection` with the cloud services before running `pip install requirements.txt` and executing the code using the cloud services terminal by running `python3 main.py`. 

When designing the solution, I initially explored the data and realized that the JSON file provided was extremely nested hence prompting me to do a draft to explore all the JSON data fully. When it came to file reading, a conventional approach like using the `CSV` module or `open` function did not work as it was an `XLSX` file type (Excel), resulting in my usage of the `pandas` module to read the Excel file. Since we are forced to use the `pandas` module, I made full use of the `pandas` module to read and the `pandas.json_normalize` function to normalize the data so that the JSON file is flattened, reducing the number of iterations needed. Additionally, I also realized that one restaurant can potentially have more than one event, and one event potentially having more than one photo link to it. 

With all this in mind, for us to get all the data needed, this solution is optimized as far as possible with the time complexity of `O(n^2)`

## Architecture Diagram
```flow
st=>start: Start
file_reading_xlsx=> operation: File reading [Country-Code.xlsx]
file_reading_json=> operation: File reading [restaurant_data.json]
loop=> condition: Has all data been accessed?
country_valid=> condition: Is the country id of the restaurant inside Country-Code.xlsx?
country_valid=> condition: Is the startdate or enddate of the event in April 2019?
extract_data_restaurant=> operation: Extract restaurant info
extract_data_events=> operation: Extract event info
file_writing_restaurant=> operation: File writing [restaurant_details.csv]
file_writing_events=> operation: File writing [restaurant_events.csv]


st->file_reading_xlsx->file_reading_json->loop
loop(no)->country_valid
loop(yes)->extract_data_restaurant->file_writing_restaurant
country_valid(yes)->extract_data_restaurant
```