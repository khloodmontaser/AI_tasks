import pandas as pd
from datetime import datetime

############################## inputs section ##############################

# first: Loading the dataset
path = '/home/lenovo/Desktop/Tasks_khloodmontaser/task1/Intern NLP Dataset.xlsx'
sheet_num = 'Sheet1'
my_dataset = pd.read_excel(path, sheet_name=sheet_num)

############################## Logic section ##############################

# second: Finding the minute with the highest number of visitors
def get_minute_with_most_visitors(dataset):
    if not pd.api.types.is_datetime64_any_dtype(dataset['Time']):
        dataset['Time'] = pd.to_datetime(dataset['Time'])

    dataset['min'] = dataset['Time'].dt.minute
    visitors_count = dataset['min'].value_counts()
    max_min = visitors_count.idxmax()
    return max_min

#third: finding the type of the most common visitors 
def get_most_common_visitor(dataset):
    visitor_types = []
    for _, row in dataset.iterrows():
        gender = 'Male' if row['Is Male'] else 'Female'
        hijab = 'Hijab' if row['Is Hijab'] else 'No Hijab'
        niqab = 'Niqab' if row['Is Niqab'] else 'No Niqab'
        child = 'Child' if row['Is Child'] else 'Adult'
        bag = 'With Bag' if row['Has Bag'] else 'No Bag'
        
        visitor_type = f"{gender}, {hijab}, {niqab}, {child}, {bag}"
        visitor_types.append(visitor_type)
    
    dataset['common type'] = visitor_types
    most_common_type = dataset['common type'].value_counts().idxmax()
    return most_common_type


#fourth: processing the input query
def query_input (query):
    query = query.lower()
    
    if "minute" in query and "most visitors" in query:
        min = get_minute_with_most_visitors(my_dataset)
        return f"the minute with the most visitors is: {min}"
    
    elif "most common visitor" in query:
        type = get_most_common_visitor(my_dataset)
        return f"the most common type of visitors: {type}"
    
    else:
        return "Error...Not Defined."
    
############################## User Interaction Section ##############################

def main():
    print("please choose an option:")
    print("1: Which minute with the most visitors?")
    print("2: Who is my most common visitor?")
    print("3: Both queries")
    
    user_choice = input("choose: ").strip()

    if user_choice == '1':
        query = "Which minute with the most visitors?"
        print(query_input(query))
    
    elif user_choice == '2':
        query = "Who is my most common visitor?"
        print(query_input(query))
    
    elif user_choice == '3':
        first_query = "Which minute with the most visitors?"
        second_query = "Who is my most common visitor?"
        print(query_input(first_query))
        print(query_input(second_query))
    
    else:
        print("invalid choice.")

############################## output section ##############################
if __name__ == "__main__":
    main()