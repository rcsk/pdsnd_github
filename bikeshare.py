import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month_selector = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    weekday_selector = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    error_catch_stmt = 'Wrong input, please try again...'
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Enter city name (chicago, new york city or washington): ').lower()
        if city.strip() in CITY_DATA:
            break
        else: print(error_catch_stmt)

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter month (all or january thru june): ').lower()
        if month.strip() in month_selector:
            break
        else: print(error_catch_stmt)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the day of week (all or monday thru sunday): ').lower()
        if day.strip() in weekday_selector:
            break
        else: print(error_catch_stmt)

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
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # Display the most common day of week
    df['day'] = df['Start Time'].dt.day
    popular_day = df['day'].mode()[0]
    print('Most Popular Day:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['day'].mode()[0]
    print('Most Popular Hour:', popular_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start)

    # Display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end)

    # Display most frequent combination of start station and end station trip
    combo_start_stop = df[['Start Station', 'End Station']].mode().loc[0]
    print('The most commonly used combined start and end station: {} + {}'.format(combo_start_stop[0], combo_start_stop[1]))
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    t_travel_time = df["Trip Duration"].sum()
    print('Total Travel Time:', t_travel_time)

    # Display mean travel time
    m_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', m_travel_time)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    c_user_types = df['User Type'].value_counts()
    print('User types:', c_user_types)

    # Display counts of gender with conditional statement due to possible incomplete dataset
    if 'Gender' in df.columns:
        c_gender = df['Gender'].value_counts()
        print('Gender Summary:', c_gender)

    # Display earliest, most recent, and most common year of birth with conditional statement due to possible incomplete dataset
    if 'Birth Year' in df.columns:
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].median()
        print('Earliest Birth Year: {}\nMost Recent Birth Year: {}\nMost Common Birth Year {}\n'.format(min_birth, max_birth, common_birth))
            
def raw_stream(df):
    """Displays the selected complete dataset."""
    # establish baseline iterator
    cont = 'yes'
    i = 0
    while cont == 'yes':
        # Prints to the user 5 lines of raw data
        print(df.iloc[i:i+5])
        # User contolled if they want to continue to see the 5 lines of raw data
        cont = input('Continue? Yes or No: \n').lower()
        i += 5
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        stream = input('\nWould you like to see the entire dataset? Enter yes or no.\n')
        if stream.lower() == 'yes':
            raw_stream(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
if __name__ == "__main__":
    main()