import analyzer
import data_sources
import data_storage
import utils
import json

def main():
    filter_options = set_filter_options()
    if get_user_input():
        display_data(filter_options)

def set_filter_options():
    filter_options_num = int(input("set the number of results to display: "))
    filter_options_sort_by = input("Enter '1' to sort by business name, '2' to sort by revenue, '3' to sort by industry, '4' to sort by distance ")
    filter_options_city = input("set the city to display: ")
    filter_options_industry = input("set the industry to display: ")
    sort_by_dictionary = {
        "1" : "business_name",
        "2" : "revenue",
        "3" : "industry",
        "4" : "distance"
    }
    filter_options = {
    "num_to_display": filter_options_num,
    "city": filter_options_city,
    "industry": filter_options_industry,
    "sort_by": sort_by_dictionary[filter_options_sort_by]
    }
    show_filters(filter_options)
    return filter_options

def show_filters(filters):
    print(f"""
Active Filters:
---------------
City: {filters['city']}
Industry: {filters['industry']}
Sort by: {filters['sort_by']}
Results to display: {filters['num_to_display']}
""")

def get_user_input():
    display = input("Do you want to dsiplay data? y/n: ")
    if display == 'y':
        return True
    return False

def display_data(filter_options):
    if filter_options["sort_by"] == "distance":
        print()
    print(filter_options['num_to_display'])
    with open("../data/sample_data.json", "r") as f:
        data = json.load(f)
    for item in data[:filter_options['num_to_display']]:
        print(f"{item['business_name']} — {item['city']}")

if __name__ == "__main__":
    main()
