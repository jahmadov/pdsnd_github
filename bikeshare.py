import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Ensures to fix possible errors in case of case-sensitive input by users.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities=list(CITY_DATA.keys())
    months = ['january','february','march','april','may','june','all']
    days = ['sunday','monday','tuesday','wednasday','thursday','friday','saturday','all']
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Please, enter the name of the city you are interested in:\n').lower()
        if city in CITY_DATA:
            break
        print('Oops! This name is not valid. Please, insert one of these names:')
        print(cities)
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month=input('Please, specify the month:\n').lower()
        if month in months:
            break
        print('Oops! This name is not valid. Please, insert one of these names:')
        print(months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Please, specify the day of the week:\n').lower()
        if day in days:
            break
        print('Oops! This name is not valid. Please, insert one of these names:')
        print(days)

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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Month']=df['Start Time'].dt.month
    months=['january','february','march','april','may','june']
    df['Weekday']=df['Start Time'].dt.day_name()
    if month!='all' and day!='all':
        df=df[df['Month']==months.index(month)+1]
        df=df[df['Weekday']==day.title()]
    elif month!='all' and day=='all':
        df=df[df['Month']==months.index(month)+1]
    elif month=='all' and day!='all':
        df=df[df['Weekday']==day.title()]
              
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Time units considered:
    - month
    - day of week
    - hour
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_match=df['Month'].mode()[0]
    print('The most frequent month for bike rent is: {}'.format(most_common_match))

    # display the most common day of week
    most_common_day=df['Weekday'].mode()[0]
    print('The most frequent weekday for bike rent is: {}'.format(most_common_day))

    # display the most common start hour
    most_common_start_hour=df['Start Time'].dt.hour.mode()[0]
    print('The most frequent start hour for bike rent is: {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_st_station=df['Start Station'].mode()[0]
    print('The most popular start station is: {}'.format(most_common_st_station))

    # display most commonly used end station
    most_common_end_station=df['End Station'].mode()[0]
    print('The most popular end station is: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Route']=df['Start Station']+' - '+df['End Station']
    most_common_route=df['Route'].mode()[0]
    print('The most popular route is: {}'.format(most_common_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt=df['Trip Duration'].sum()
    print('Total trip duration is: ' + str(ttt//(24*3600)) + ' days ' + str((ttt%(24*3600))//3600) + ' hours ' + str((ttt%3600)//60) + ' minutes ' + str(ttt%60) + ' seconds')

    # display mean travel time
    mtt=df['Trip Duration'].mean()
    print('Average trip duration is: ' + str(int(mtt//60)) + ' minutes ' + str(int(mtt%60)) + ' seconds ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type=df['User Type'].value_counts()
    print('Count of bikeshare user types is:\n{}'.format(count_user_type))

    # Display counts of gender
    if 'Gender' not in df:
        print('Gender information is not found for this city')
    else:
        count_gender=df['Gender'].value_counts()
    print('\nCount of bikeshare users per gender is:\n{}'.format(count_gender))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('Birth year information is not found for this city')
    else:
        earliest=int(df['Birth Year'].min())
        most_recent=int(df['Birth Year'].max())
        most_common=int(df['Birth Year'].mode()[0])
        print('\nEarliest year of birth is: {}'.format(earliest))
        print('Most recent year of birth is: {}'.format(most_recent))
        print('Most common year of birth is: {}'.format(most_common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    raw_data_inp=input("Do you want to see the raw data? Please, specify your answer with yes or no:")
    line_count=0
    
    while True:
        if raw_data_inp.lower()=='yes':
            print(df.iloc[line_count:line_count+5])
            line_count+=5
            raw_data_inp=input("Do you want to see the raw data? Please, specify your answer with yes or no:")
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
