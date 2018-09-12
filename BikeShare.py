
# coding: utf-8

# # BikeShare
# 
# I am using a Jupyter Notebook here to work on this project and comment on the code in the sense of literate programming.
# 
# First, I import relevant packages to work on the project.

# In[7]:


import time
import pandas as pd
import numpy as np


# Next, I build the CITY DATA dictionary consisting of the data handed over in the three csv files.

# In[8]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# I check out the structure of the data, looking at the first 5 rows.

# In[9]:


df = pd.read_csv("chicago.csv")
print(df.head())


# The following function is asking the use to specify a city, month and day to analyze.
# It will return: 
#         (str) city - name of the city to analyze
#         (str) month - name of the month to filter by, or "all" to apply no month filter
#         (str) day - name of the day of week to filter by, or "all" to apply no day filter.
# It also prompts the user to re-enter if the entry was not correct.

# In[10]:


def get_filters():
   
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('What city data would you like to analyze? Enter "chicago", "new york city", "washington" or "all": ').lower() 
    while city not in ("chicago", "new york city", "washington", "all"):
        city = input('This is not a valid input. Please enter "chicago", "new york city", "washington" or "all": ')
    else: 
        print('Thank You! We will analyze data for {} for you'.format(city)) 
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('What month would you like to analyze? Enter the name of the month or "all" for no month filter: ').lower()
    while month not in ('january', 'february', 'march', 'april', 
                        'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all'):
        month = input('This is not a valid input. Enter the name of the month or "all" for no month filter: ')
    else: 
        print('Thank You! We will analyze data for {} for you'.format(month))
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('What day of the week would you like to analyze? Enter the name of the day or "all" for no day filter: ').lower()
    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input('This is not a valid input. Enter the name of the month or "all" for no month filter: ')
    else: 
        print('Thank You! We will analyze data for {} for you'.format(day))

    print('-'*40)
    return city, month, day





# Loading selected data and applying filters corresponding to input provided by user.

# In[11]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

city, month, day = get_filters()
load_data(city, month, day).head()


# Prompt the user to check 5 lines of raw data and include exception for 'Gender' and 'Birth Year'
# 
# 

# In[12]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    df = load_data(city, month, day)
    # ToDo: here I will have to adjust for month (etc.) names vs. indices...!
    # TO DO: display the most common month: The month as January=1, December=12
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # TO DO: display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.dayofweek
    popular_day = df['day'].mode()[0]
    print('Most Popular Start Day:', popular_day)

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    return time_stats 
   

time_stats(df)
print('-'*40)



# In[13]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    df = load_data(city, month, day)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_ss = df['Start Station'].mode()[0]
    print('Most popular start station', popular_ss)

    # TO DO: display most commonly used end station
    popular_es = df['End Station'].mode()[0]
    print('Most popular end station', popular_es)

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most popular combination', popular_trip)
    
    return station_stats

station_stats(df)
print('-'*40)


# In[14]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    df = load_data(city, month, day)
    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total travel time: ', total_duration)
    
    # TO DO: display mean travel time
    average_duration = df['Trip Duration'].mean()
    print('Average travel time: ', average_duration)
    
    return trip_duration_stats

trip_duration_stats(df) 
print('-'*40)


# In[16]:


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try: 
        df = load_data(city, month, day)
        # TO DO: Display counts of user types
        count_user_type = df.groupby(['User Type']).count()
        print('Count of user type: ', count_user_type)

        # TO DO: Display counts of gender
        count_gender = df.groupby(['Gender']).count()
        print('Count of gender: ', count_gender)

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        print('Earliest birth year: ', earliest)

        recent = df['Birth Year'].max()
        print('Most recent birth year: ', recent)

        common = df['Birth Year'].mode()[0]
        print('Most common birth year: ', common)
    
    except KeyError:
        df = load_data(city, month, day)
        # TO DO: Display counts of user types
        count_user_type = df.groupby(['User Type']).count()
        print('Count of user type: ', count_user_type)
    
    
    return user_stats

user_stats(df)
print('-'*40)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

