from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
    def __init__(self, name, date):
        self._name = name
        self._date = date

    def __str__ (self):
        # String output
        _output = str()(self._name) + ', ' + str(self._date)
        # Holiday output when printed.
        return _output
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    
    def __init__(self):
       self.innerHolidays = []
   

    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if type(holidayObj) == Holiday:
        # Use innerHolidays.append(holidayObj) to add holiday
            self.innerHolidays.append(holidayObj)
        # print to the user that you added a holiday
            print('Holiday added!')
        else:
            print('Error. Not a holiday.')
        return


    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for item in self.innerHolidays:
            if item._name == HolidayName and item._date == Date:
        # Return Holiday
                return item


    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        holiday_remove = self.findHoliday(HolidayName, Date)
        # remove the Holiday from innerHolidays
        if holiday_remove != None:
            self.innerHolidays.remove(holiday_remove)
        # inform user you deleted the holiday
            print('Holiday removed!')
            return
        else:
            print('Holiday not found.')
            return


    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, 'r') as f:
            x = json.loads(f.read())
        # Use addHoliday function to add holidays to inner list.
        addHoliday = x['holidays']
        for i in range(len(addHoliday)):
            current = addHoliday[i]
            tempDate = datetime.strptime(current['date'], '%Y-%m-%d')
            tempName = current['name']
            self.innerHolidays.append(Holiday(tempName, tempDate))
        return


    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation, 'w', encoding='utf-8') as j:
            output_list = []
            for item in self.innerHolidays:
                temp = {}
                temp['name'] = item._name
                temp['date'] = str(item._date)
                output_list.append(temp)
            json.dump(output_list, j, indent = 4)
        print('File saved.')
        j.close()
        return

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        yearList = [2020, 2021, 2022, 2023, 2024]
        for year in yearList:
            html = requests.get(f"https://www.timeanddate.com/holidays/us/{year}?hol=33554809")
            soup = BeautifulSoup(html.text,'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            for row in rows:
                tempDate = row.find('th').text, year
                formatDate = datetime.strptime(
                    '%s %s' % tempDate, 
                    '%b %d %Y',
                )
                date = formatDate.strftime('%Y-%m-%d')
                name = row.find('a').text
                newHoliday = Holiday(name, date)
                self.innerHolidays.append(newHoliday)
        return

        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.   (try/except)  


    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        holidayCount = len(self.innerHolidays)
        print('There are ' + str(holidayCount) + ' holidays stored in the system.' )
        return holidayCount
    

    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        filterHolidays = list(filter(lambda x: x.date.isocalendar()[1] == week_number 
            and x.date.isocalendar()[0] == year, self.innerHolidays))
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        return filterHolidays


    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        for i in holidayList:
            print(i)
        # Output formated holidays in the week. 
        return


    # def getWeather(self, weekNum):
    #     # Convert weekNum to range between two digits (weeknum 1 - weeknum 52)
    #     # Use Try / Except to catch problems
    #     # Query API for weather in that week range
    #     # check if weekdisplay is in the current week; if so, getweather
    #     # Format weather information and return weather string.
    #     ##### unable to complete.


    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        c = datetime.now()
        current_Week = c.isocalendar().week
        current_Year = c.isocalendar().year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        holidaysWeek = self.filter_holidays_by_week(current_Year, current_Week)
        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidaysInWeek(holidaysWeek)
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        return

def menuAdd(HolidayList):
    saveHoliday = False
    print('Add a Holiday')
    print('=============')
    # user input for holiday name and holiday date
    while saveHoliday == False:
        addInput = input('Using only alpha characters, please enter the name of the holiday: ')
        if type(addInput) != str:
            print('Please try again using only alpha characters.')
        else:
            print('Holiday: ' + str(addInput))
            print('Moving onto date...')
        # change format of date using strptime
        dateInput = input('Using YYYY-MM-DD format, please enter the date of the holiday: ')
        dateFormat = datetime.strptime(dateInput, '%Y-%m-%d')
        if type(dateFormat) != datetime:
            print('Error: ')
            print('Invalid date. Please try again.')
            saveHoliday = False
            return saveHoliday
        else:
            print('Date for ' + str(addInput) + ': ' + str(dateFormat))
            print('Checking...')
        # check holidaylist for dupe
        if HolidayList.findHoliday(addInput, dateFormat) == None:
            HolidayList.addHoliday(Holiday(addInput, dateFormat))
            saveHoliday = True
            print('Success: ')
            print(str(addInput) + ' ' + str(dateFormat) + ' has been added to the holiday list.')
            return saveHoliday
        else:
            print('Oops! This holiday has been previously saved.')
            saveHoliday = False
            return saveHoliday
        # return to menu
    return

def menuRemove(HolidayList):
    removeHoliday = False
    print('Remove a Holiday')
    print('=============')
    # user input for holiday name and holiday date
    while removeHoliday == False:
        removeInput = input('Using only alpha characters, please enter the name of the holiday: ')
        if type(removeInput) != str:
            print('Please try again using only alpha characters.')
        else:
            print('Holiday Name: ' + str(removeInput))
            print('Moving onto date...')
        # change format of date using strptime
        dateInput = input('Using YYYY-MM-DD format, please enter the date of the holiday: ')
        dateFormat = datetime.strptime(dateInput, '%Y-%m-%d')
        if type(dateFormat) != datetime:
            print('Please try again using the correct format.')
            removeHoliday = False
            return removeHoliday
        else:
            print('Working...')
    # send to removeholiday() holiday name and holiday date
        if HolidayList.findHoliday(removeHoliday, dateFormat) != None:
            HolidayList.removeHoliday(Holiday(removeInput, dateFormat))
            removeHoliday = True
            print('Success: ')
            print('/n')
            print(str(removeInput) + ' ' + str(dateFormat) + ' has been removed to the holiday list.')            
            return removeHoliday
        else:
            print('Oops! This holiday has not been previously saved and therefore cannot be removed.')
            removeHoliday = False
            return removeHoliday
    # return to menu
    return

def menuView(HolidayList):
    print('View Holidays')
    print('=================')
    # variable for current date
    current_week = datetime.now().isocalendar()[1]
    current_year = datetime.now().year
    yearView = False
    weekView = False
    # user input for year
    while yearView == False:
        yearInput = input('Which year?: ')
        yearInput = int(yearInput)
        if yearInput > 2019 and yearInput < 2025:
            yearView = True
            print('Working...')
        else:
            print('Please choose a year between 2019-2024 and input the year as four digits. Ex: 2022')
    # user input for week number (print link epoch converter site)
    while weekView == False:
        print('If you need help finding the week number: https://www.calendar-365.com/week-number.html ')
        weekInput = input('Which week?: ')
        weekInput = int(weekInput)
        if weekInput == current_week and yearInput == current_year:
            HolidayList.viewCurrentWeek()
            weekView = True
        elif weekInput > 0 and weekInput < 53:
            print('These are the holidays: ')
            HolidayList.displayHolidaysInWeek(HolidayList.filter_holidays_by_week(yearInput, weekInput))
            weekView = True
            return weekView
        else:
            print('Error. Issue with week input. Try again.')
    return
    # validate user inputs
    # use displayHolidaysInWeek() to display if valid inputs
    # return to menu


def menuSave(HolidayList):
    # file location
    filelocation = 'new_holidays.json'
    print('Saving Holiday List')
    print('====================')
    # print that file is saving
    userSave = False
    # user input confirming theyd like to exit y/n
    while userSave == False:
        saveInput = input('Are you sure you want to save your changes? Yes/No: ')
    # if n, end loop
        if 'n' in saveInput.lower():
            print('Canceled:')
            print('Holiday list file save canceled.')
            return
        if 'y' in saveInput.lower():
            print('Working...')
            print('Success:')
            HolidayList.save_to_json(filelocation)
            print('Your changes have been saved.')
            userSave = True
            return userSave
    # return to menu
    return

def menuExit():
    print('Exit')
    print('=====')
    userExit = False
    # user input confirming theyd like to exit y/n
    while userExit == False:
        exitInput = input('Are you sure you want to exit? Your changes will be lost. Yes/No: ')
    # if y, end loop
        if 'y' in exitInput.lower():
            print('Goodbye!')
            userExit = True
            useManager = False
    # if no, return to menu
        elif 'n' in exitInput.lower():
            print('Returning to menu...')
            return
        else:
            print('Sorry, issue occurred.')
    return useManager

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # print Start Up text, return number of holidays from holiday list
    print('Holiday Management')
    print('===================')
    # 1. Initialize HolidayList Object
    mainHolidayList = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    mainHolidayList.read_json('holidays.json')
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    mainHolidayList.scrapeHolidays()
    mainHolidayList.numHolidays()
    # 4. Display User Menu (Print the menu)
    # print Main Menu text
    print('Holiday Menu')
    print('================')
    print('1. Add a Holiday')
    print('2. Remove a Holiday')
    print('3. Save Holiday List')
    print('4. View Holidays')
    print('5. Exit')
    # 3. Create while loop for user to keep adding or working with the Calender
    # use while loop
    useManager = True
    while useManager == True:
        menuOption = False
        menuInput = input('Please enter the number of the action you would like to do: ')
        while menuOption == False:
            if menuInput is not int:
                menuInput = int(menuInput)
            else:
                continue
            if menuInput == 1:
                menuAdd(mainHolidayList)
                menuOption = True
            elif menuInput == 2:
                menuRemove(mainHolidayList)
                menuOption = True
            elif menuInput == 3:
                menuSave(mainHolidayList)
                menuOption = True
            elif menuInput == 4:
                menuView(mainHolidayList)
                menuOption = True
            elif menuInput == 5:
                useManager = menuExit()
                menuOption = True
            else:
                print('Oops! Error occurred. Please try again.')

    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





