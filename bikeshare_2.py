import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# NOTE: the program uses the Pandas 'mode' function in multiple places and references index 0 on the series it produces
# The mode function works correctly when there are results with more than one occurance, but produces an empty series if
# all results occur only once. Additional coding would be necessary to produce a usable response for a dataset containing
# datapoints that only appear once.

def raw_or_statistical_data():
    """
    Begins by giving the user the option to view individual trip data 5 rows at a time or view statistical data from the whole dataset.

    If the user selects to view statistical data, the function exits and progresses to selecting filters and displaying the appropriate info.

    If the user selects to view individual trip data, the user will first select a city before 5 rows of trip data is displayed.
    The user will then need to select to view 5 more rows, or exit to loop back to the option to view trip data or statistical data.

    Returns:
        (str) selection - user selection to launch raw data functions or statistical data functions
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        selection = input("Would you like to view individual trip data (5 rows at a time) or statistical data? Select: (raw data, statistical data) ").lower()
        if selection != 'raw data' and selection != 'statistical data':
            # user either attempted to select an unavailable option or made a typo, so we return to the loop
            print("Sorry, please select an available option and be sure to type it exactly as it appears.")
            continue
        if selection == 'statistical data':
            # user selects statistical data and we break the loop to transition to the statistical functions
            break
        if selection == 'raw data':
            # user selects raw data and we break the loop to transition to the raw data functions
            break

    print('-'*40)
    return selection

def view_data():
    # get user input for city to view raw data
    while True:
        options = ['chicago', 'new york city', 'washington']
        city = input("Please select a city and type exactly as it appears: (chicago, new york city, washington) ").lower()
        if city not in options:
            # user either selected a city that is not available or made a typo, so we return to the start of the loop
            print("Sorry, please select an available option and be sure to type it exactly as it appears.")
            continue
        else:
            # city selection was successful and we exit the loop
            break
    # load the selected city data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # set the starting row location
    start_loc = 0
    # set the view_display selection to begin the loops that give the user the ability to view more raw data or exit viewing raw data
    view_display = ''
    while view_display != 'exit':
        # check current display location against the total number of rows in the dataframe
        if start_loc + 5 > len(df.index):
            print("You have reached the end of the available data. The following are the final available rows of data.")
            print(df.iloc[start_loc:])
            break
        if start_loc + 5 < len(df.index):
        # print the next 5 rows of data from the selected city
            print(df.iloc[start_loc:(start_loc + 5)])
        # get user input on showing 5 more rows of data or breaking the loop to return to the raw data or statistical data choice
        while True:
            view_display = input("Do you want to see 5 more rows of data? Select: (continue, exit) ").lower()
            if view_display != 'continue' and view_display != 'exit':
                # user either attempted an invalid option or made a typo, so we restart the selection loop
                print("Sorry, please select an available option and be sure to type it exactly as it appears.")
                view_display = ''
                continue
            if view_display == 'continue':
                # user selected to show more raw data, so we advance the starting location and return to print more data
                start_loc += 5
                view_display = ''
                break
            if view_display == 'exit':
                # user selected to exit viewing raw data, so we break the internal loop without redefining view_display so we also break the outer loop
                break

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        options = ['chicago', 'new york city', 'washington']
        city = input("Please select a city and type exactly as it appears: (chicago, new york city, washington) ").lower()
        if city not in options:
            # user either selected a city that is not available or made a typo, so we return to the start of the loop
            print("Sorry, please select an available option and be sure to type it exactly as it appears.")
            continue
        else:
            # city selection was successful and we exit the loop
            break


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
            options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
            month = input("Please select a month on which to filter (or select 'all' to apply no month filter): (january, february, ... , june) ").lower()
            if month not in options:
                # user either selected a month that is not available or made a typo, so we return to the start of the loop
                print("Sorry, please select an available option and be sure to type it exactly as it appears.")
                continue
            else:
                # month selection was successful and we exit the loop
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = input("Please select a day on which to filter (or select 'all' to apply no day filter): (monday, tuesday, ... , sunday) ").lower()
            if day not in options:
                # user either selected a day that is not available or made a typo, so we return to the start of the loop
                print("Sorry, please select an available option and be sure to type it exactly as it appears.")
                continue
            else:
                # day selection was successful and we exit the loop
                break

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

    # create a dataframe using the city selection from user input
    df = pd.read_csv(CITY_DATA[city])

    # turn the Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new columns for month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name

    # check to apply a month filter
    if month != 'all':
        # get numerical representation of month through an index
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # check to apply a day filter
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is: {month}".format(month=most_common_month))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {day}".format(day=most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common hour is: {hour}".format(hour=most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {station}".format(station=most_common_start))

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print("The most commonly used end station is: {station}".format(station=most_common_end))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combo = df[['Start Station', 'End Station']].mode()
    print("The most commonly used start/end station combo is: start - {start}, end - {end}".format(start=most_common_combo.at[0, 'Start Station'], end=most_common_combo.at[0, 'End Station']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: {duration} minutes".format(duration=total_travel_time))

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The average travel time is: {duration} minutes".format(duration=mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    sub_count = df.loc[df['User Type'] == 'Subscriber', 'User Type'].count()
    customer_count = df.loc[df['User Type'] == 'Customer', 'User Type'].count()
    print("The total number of subscribers is: {subscribers}. The total number of customers is: {customers}.".format(subscribers=sub_count, customers=customer_count))

    # TO DO: Display counts of gender
    if 'Gender' in df:
        num_male = df.loc[df['Gender'] == 'Male', 'Gender'].count()
        num_female = df.loc[df['Gender'] == 'Female', 'Gender'].count()
        print("The total number of male subscribers is: {males}. The total number of female subscribers is: {females}.".format(males=num_male, females=num_female))
    else:
        print("Gender statistics are not available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df["Birth Year"].min())
        latest_birth_year = int(df["Birth Year"].max())
        most_common_birth_year = int(df["Birth Year"].mode()[0])

        print("The earliest birth year is: {earliest}".format(earliest=earliest_birth_year))
        print("The most recent birth year is: {recent}".format(recent=latest_birth_year))
        print("The most common birth year is: {common}".format(common=most_common_birth_year))
    else:
        print("Birth Year statistics are not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        selection = raw_or_statistical_data()
        if selection == 'raw data':
            view_data()

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

        if selection == 'statistical data':
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
