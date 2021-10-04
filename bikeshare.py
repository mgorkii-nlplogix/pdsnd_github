import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ('january', 'february', 'march', 'april', 'may', 'june')

days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday')
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
  
    # get user input for city (chicago, new york city, washington)
    while True:
        city, month, day = None, None, None
        
        # make sure the user enters the city 
        while (city not in CITY_DATA) and (city != 'new york') :
            city = str(input("Would you like to see data for Chicago, New York, or Washington? ")).lower().strip()
            if city == 'new york':
                city = 'new york city'

        # get the filter from the user
        filter = str(input("Would you like to filter the data by month, day, or not at all? ")).lower().strip()
        if filter == 'month':   
            while month not in months and month != 'all':
                month = str(input("Which month - January, February, March, April, May, or June ")).lower().strip()
                if month == 'all':
                    month = None
                    break
 
        elif filter == 'day':
            while day not in days and day != 'all':
                day = str(input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?")).lower().strip()
                if day == 'all':
                    day = None
                    break

        else:
            no_filter = input('\nWould you like to continue with no filters? Enter yes or no.\n')
            if no_filter.lower() != 'yes':
                continue

        print('-'*40)
        return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
   
    # load data file into a dataframe
    df = pd.read_csv (CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month is not None:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day is not None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('\nThe most common month for applied filter is : ' + str(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day for applied filter is : ' + common_day)
    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    common_start_hour = df['Start Hour'].mode()[0]
    print('The most common start hour for applied filter is : ' + str(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = str(df['Start Station'].mode()[0])
    print('\nThe most commonly used start station : ' + common_start_station)

    # display most commonly used end station
    common_end_station = str(df['End Station'].mode()[0])
    print('The most commonly used end station : ' + common_end_station)
    # display most frequent combination of start station and end station trip
    df['Start and End Combination'] = (df['Start Station'] + df['End Station'])
    common_start_end_comb = str(df['Start and End Combination'].mode()[0])
    print ('The most commonly used combination of start and end station : ' + common_start_end_comb)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('\nTotal travel time for the selected filter : ' + str(total_time))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print ('Average travel time for the selected filter : ' + str(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('\nCounts of user types for selected filter : ' + '\n' + str(user_types_count))

    # Display counts of gender
    try: 
        user_gender_count = df['Gender'].value_counts()
        print ('Counts of Gender for selected filter : ' + '/n' + str(user_gender_count))

    except KeyError:
        print("There is no gender data for {} database.".format(city))

    # Display earliest, most recent, and most common year of birth
    def no_birth_data():
        print("Sorry, there is no birth data in {} database.".format(city))

    try:
        earliest_year = df['Birth Year'].min()
        print ('The olders rider as born in : ' + str(earliest_year))
        
    except KeyError:
        no_birth_data()
    
    try:
        recent_year = df['Birth Year'].max()
        print('The youngest rider was born in : ' + str(recent_year))
    except KeyError:
        no_birth_data()

    try:
        common_year = df['Birth Year'].mode()[0]
        print('Most common year of users birth : ' + str(common_year))
    except KeyError:
        no_birth_data()
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data on user request"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no?')
    if view_data != 'yes':
        return
    else: 
        print(df.head())
        start_loc = 0
        while True:
            view_more_data = input('\nWould you like to view 5 more rows of individual trip data? Enter yes or no?')
            if view_more_data.lower() != 'yes':
                break
            else: 
                start_loc +=5
                print(df.iloc[start_loc:start_loc+5])
                continue



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()