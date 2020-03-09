import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

correct_cities=['chicago', 'washington', 'new york']
correct_months= ['january', 'february', 'march', 'april', 'may', 'june']
correct_days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('Please enter the city you want to explore. Enter chicago, new york, or washington: ').lower()
    while city not in correct_cities:
        print('Oops! This city is invalid. Please try again by entering chicago, new yor or washington: ')
        city=input('Please enter the city you want to explore. Enter chicago, new york, or washington: ').lower()
    else:
         # TO DO: get user input for month (all, january, february, ... , june)
        month= input("Would you like to filter by month? If yes, enter january, february, march, april, may or june. If you would not like to fulter vy month, enter all: ").lower()
        while month not in correct_months:
            print('Oops! This month is invalid. Please try again by entering january, february, march, april, may or june. ')
            month= input("Would you like to filter by month? If yes, enter january, february, march, april, may or june. If you would not like to filter by month, enter all: ").lower()
            print("Exploring data for {}.".format(month).lower())
        #TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day=input('Would you like to filter by day? If yes, enter monday, tuesday, wednesday, thursday, friday or saturday. If not, enter all: ').lower()
        while day not in correct_days:
            print('Oops! This day is invalid. Please try again by entering monday, tuesday, wednesday, thursday, friday or saturday.')
            day=input('Would you like to filter by day? If yes, enter monday, tuesday, wednesday, thursday, friday or saturday. If not, enter all: ').lower()
            print('Exploring data for {}.'.format(day).lower())
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
    df['month']=df['Start Time'].dt.month_name().str.lower()
    df['day_of_week']= df['Start Time'].dt.weekday_name
    if month != 'all':
        df = df[df['month']== month]
    if day !='all':
        df=df[df['day_of_week']== day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    common_month= df['Start Time'].mode()[0]
    print('Most popular month: ', common_month)
    # TO DO: display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print('Most popular day of the week: ', common_day)
    # TO DO: display the most common start hour   .dt.hour
    common_s_hour=df['Start Time'].dt.hour.mode()[0]
    print('Most popular start hour: ', common_s_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return common_month, common_day, common_s_hour

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    pop_start_station= df['Start Station'].mode()[0]
    print('Most popular start station: ', pop_start_station)
    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', pop_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    freq_combination=df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station: ', freq_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return pop_start_station, pop_end_station, freq_combination


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    sum_travel_time =df.groupby(['month', 'day_of_week'])['Trip Duration'].sum()
    print('Total travel time: ',sum_travel_time)
    # TO DO: display mean travel time
    avg_travel_time=df.groupby(['month', 'day_of_week'])['Trip Duration'].mean()
    print('Mean travel time: ',avg_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return sum_travel_time,avg_travel_time


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if city== 'washington':
          print('There is no userdata for Washington')
    else:
          user_type = df['User Type'].value_counts()
          print('User types in data: ', user_type)
          # TO DO: Display counts of gender
          gender = df['Gender'].value_counts()
          print('Gender count: ', gender)
          # TO DO: Display earliest, most recent, and most common year of birth
          earliest_year_birth = df['Birth Year'].min()
          print('Earliest year of birth: ', earliest_year_birth)
          most_recent_year_birth = df['Birth Year'].max()
          print('Most recent birth year:', most_recent_year_birth)
          common_year_birth=df['Birth Year'].mode()[0]
          print('Most common year of birth: ', common_year_birth)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        my_count=0
        while True:
            view_rows= input('Do you want to see 5 rows of data? Please answer yes or no: ').lower()
            if (view_rows=='yes'):
                print(df.iloc[my_count:(my_count+5)])
                my_count=my_count+5
            else:
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
