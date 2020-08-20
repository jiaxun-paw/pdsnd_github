import time
import pandas as pd
import numpy as np
import calendar as c

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter city (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city entered.\n')
            # repeat user input request

    # get user input for month (all, january, february, ... , june)
    valid_months = list(c.month_name)
    valid_months.append('all')
    valid_months = [month_name.lower() for month_name in valid_months]

    while True:
        month = input('Please enter month (all, january, february, ... , june): ').lower()
        if valid_months.count(month) != 0:
            break
        else:
            print('Invalid city entered.\n')
            # repeat user input request

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = list(c.day_name)
    valid_days.append('all')
    valid_days = [day_name.lower() for day_name in valid_days]

    while True:
        day = input('Please enter day of week (all, monday, tuesday, ... sunday): ').lower()
        if valid_days.count(day) != 0:
            break
        else:
            print('Invalid day entered.\n')
            # repeat user input request

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
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = [e.lower() for e in c.month_name]
        del months[0]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df.month == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # Month created when loading data
    print('Most Popular Month:', df['month'].mode()[0])

    # display the most common day of week
    # Day of week created when loading data
    print('Most Popular Day of Week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    print('Most Popular Start Hour:', df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    has_start = 'Start Station' in df.columns
    has_end = 'End Station' in df.columns

    if has_start:
        # display most commonly used start station
        print('Most Commonly Used Start Station:', df['Start Station'].mode()[0])
    else:
        print('No data for start station. Skipping calculation and display of statistics on start station.')

    if has_end:
        # display most commonly used end station
        print('Most Commonly Used End Station:', df['End Station'].mode()[0])
    else:
        print('No data for end station. Skipping calculation and display of statistics on end station.')

    if has_start and has_end:
        # display most frequent combination of start station and end station trip
        trips = df['Start Station'] + ' / ' + df['End Station']
        print('Most Frequent Combination of Start Station and End Station Trip:', trips.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df.columns:
        # display total travel time
        total_time = format_time(df['Trip Duration'].sum())
        print('Total travel time: {} day(s), {} hour(s), {} minute(s), {} second(s)'.format(total_time[0], total_time[1], total_time[2], total_time[3]))

        # display mean travel time
        mean_time = format_time(int(round(df['Trip Duration'].mean())))
        print('Mean travel time: {} day(s), {} hour(s), {} minute(s), {} second(s)'.format(mean_time[0], mean_time[1], mean_time[2], mean_time[3]))
    else:
        print('No data for trip duration. Skipping calculation and display of statistics on trip duration.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_time(total_seconds):
    """
    Formats time in seconds into a tuple (days, hours, minutes, seconds).

    Args:
        (int) seconds - amount of time to format
    Returns:
        (days, hours, minutes, seconds) - Tuple with a breakdown of the time supplied.
    """
    days, remaining_time = divmod(total_seconds, 86400)
    hours, remaining_time = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remaining_time, 60)
    return (days, hours, minutes, round(seconds))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('Counts of Users Types:')
        print(df['User Type'].value_counts())
    else:
        print('No data for user types. Skipping calculation and display of statistics on user types.')
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of Gender:')
        print(df['Gender'].value_counts())
    else:
        print('No data for gender. Skipping calculation and display of statistics on gender.')
    print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest birth year: ', df['Birth Year'].min())
        print('Recent birth year: ', df['Birth Year'].max())
        print('Most common birth year: ', df['Birth Year'].mode()[0])
    else:
        print('No data for birth year. Skipping calculation and display of statistics on birth year.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        current_row = 0
        while True:
            to_display = input('\nWould you like to display ' + ('another ' if current_row != 0 else '') + '5 rows of the data? Enter yes or no.\n')
            if to_display.lower() == 'yes':
                print(df[current_row:current_row+5])
                print('-'*40)
                current_row += 5
            else:
                break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
