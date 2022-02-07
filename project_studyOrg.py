#!/bin/python3

import TextFileReader as tfr
from tabulate import tabulate
import calendar
import time
from datetime import datetime
from itertools import groupby
from copy import deepcopy
from colorama import Fore, Back, Style

grades_header = []
grades = []
timetable_header = []
timetable = []
appointments_header = []
appointments = []
modules = []
modules_header = []
notes = []
notes_header = []
modulenames = []

today = datetime.today()

menu_options = {
    1: 'Home',
    2: 'Module',
    3: 'Calendar',
    4: 'Grades',
    5: 'Exit',
}

menu_options_home = {
    1: 'Daily appointments',
    2: 'Notes',        # TODO edit, delete and send notes -> more fnctionalitys possible
    3: 'Worktimer',    # TODO collect time per module or project
    4: 'Go back',
}

menu_options_notes = {
    1: 'Add new note',
    2: 'Show notes',
    3: 'Go back',
}

menu_options_modul = {
    1: 'Add new Modul or Project',
    # TODO numbered urls + open link by enter number
    2: 'Search for Modul or Project',
    3: 'Go back',
}

menu_options_calendar = {
    1: 'Display actual month',
    2: 'Show timetable',
    3: 'Show appointments',
    4: 'Add appointments',
    5: 'Today',
    6: 'Go back',
}

menu_options_grades = {
    1: 'Show Grades',
    2: 'Add Grades',
    3: 'Grade average',
    4: 'Go Back',
}

# ------------------ Menus ------------------


def print_menu(options):
    ''' Shows menu and gets input.
    '''
    for key in options.keys():
        print(key, '--', options[key])


def home():
    ''' Shows the home submenu and gets input.
    '''
    while True:
        print(Fore.BLACK + Back.GREEN +
              'Welcome Home!                            ' + Style.RESET_ALL)
        print_menu(menu_options_home)

        option = ''

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
            show_today()
        elif option == 2:
            take_notes()
        elif option == 3:
            work_timer()
        elif option == 4:
            return
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


def module():
    ''' Shows the module submenu and gets input.
    '''
    while True:
        print(Fore.BLACK + Back.GREEN +
              'MODULES AND PROJECTS                     ' + Style.RESET_ALL)
        print_menu(menu_options_modul)

        option = ''

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
            add_new_modul()
        elif option == 2:
            search_modul()
        elif option == 3:
            return
        else:
            print('Invalid option. Please enter a number between 1 and 3.')


def calendar_overview():
    ''' Shows the calendar submenu and gets input.
    '''
    while True:
        delete_old_appointments()

        print(Fore.BLACK + Back.GREEN +
              'Calendar                                 ' + Style.RESET_ALL)
        print_menu(menu_options_calendar)

        option = ''

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
            show_month()
        elif option == 2:
            print(Fore.BLACK + Back.GREEN +
                  'Timetable                            ' + Style.RESET_ALL)
            show_list_with_header(timetable, timetable_header)
        elif option == 3:
            show_appointments()
        elif option == 4:
            try:
                add_appointment()
            except ValueError:
                print('wrong input try again')
        elif option == 5:
            show_today()
        elif option == 6:
            return
        else:
            print('Invalid option. Please enter a number between 1 and 6.')


def grades_overview():
    ''' Shows the grades submenu and gets input.
    '''
    while True:
        print(Fore.BLACK + Back.GREEN +
              'Grades                                   ' + Style.RESET_ALL)
        print_menu(menu_options_grades)

        option = ''

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
            print(Fore.BLACK + Back.GREEN +
                  'All Grades                           ' + Style.RESET_ALL)
            show_list_with_header(grades, grades_header)
        elif option == 2:
            add_grade()
        elif option == 3:
            grades_average()
        elif option == 4:
            return
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

# ------------------ Data and Files ------------------


def save_data():
    ''' Writes all used lists in files.
    '''
    write_file('grades.txt', grades, grades_header)
    write_file('appointments.txt', appointments, appointments_header)
    write_file('modules.txt', modules, modules_header)
    write_file('notes.txt', notes, notes_header)


def write_file(file_name, data_list, list_header):
    ''' Writes list and list header in the given .txt file.

        Args:
            file_name (string) : name of the .txt file
            data_list (list) : list with the data which should be written in the file
            list_header (list) : headline of the data which should be written in the file
    '''
    if any(data_list):
        # open file in write modus
        with open(file_name, 'w') as f:
            # generate comma seperated string of the headerline
            line = ','.join(str(x) for x in list_header[0])
            # write line in file
            f.write(line + '\n')

            # go through the whol data list and write line per line
            for sublist in data_list:
                line = ','.join(str(x) for x in sublist)
                f.write(line + '\n')
            # close file
            f.close()


def fill_data():
    ''' Reads all data from the files into lists.
    '''
    read_file('grades.txt', grades, grades_header)
    read_file('appointments.txt', appointments, appointments_header)
    read_file('timetable.txt', timetable, timetable_header)
    read_file('modules.txt', modules, modules_header)
    read_file('notes.txt', notes, notes_header)
    # identify all different modules
    get_modules()


def read_file(file_name, data_list, list_header):
    ''' Reads the given .txt file and put data in list and list header.
        Use the provided TextReader.py from the lectures

        Args:
            file_name (string) : name of the .txt file
            data_list (list) : list for the data from the file
            list_header (list) : list for the headline from the file
    '''
    # open file
    file = tfr.open_file(file_name)
    # get headline frome the first line in the file
    headitems = tfr.get_line_items(file, ',')
    list_header.append(headitems)

    # go through the whole file and put line per line in list
    while True:
        items = tfr.get_line_items(file, ',')
        if items == None:
            break
        data_list.append(items)
    # close file
    tfr.close_file(file)

# ------------------ Home functions ------------------


def take_notes():
    ''' Shows the notessubmenu and gets input.
    '''
    print(Fore.BLACK + Back.GREEN +
          'NOTES MENU                                   ' + Style.RESET_ALL)
    print_menu(menu_options_notes)

    option = ''

    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')

    # Check what choice was entered and act accordingly
    if option == 1:
        add_notes()
    elif option == 2:
        show_notes()
    elif option == 3:
        return()
    else:
        print('Invalid option. Please enter a number between 1 and 3.')


def show_notes():
    ''' Shows all notes and there titles.
    '''
    print(Fore.BLACK + Back.GREEN +
          'SHOW NOTES                                   ' + Style.RESET_ALL)
    print(tabulate(notes))


def add_notes():
    ''' Add a new note with title.
    '''
    print(Fore.BLACK + Back.GREEN +
          'ADD NEW NOTES                                ' + Style.RESET_ALL)
    notetitle = input('Enter a Title or Modul as a header: ')
    usernote = input('Enter ur notes: ')
    print('')

    notes.append([notetitle, usernote])


def countdown(time_sec):
    ''' Start the countdowntimer with the input time.

        Args:
            time_sec (int) : time in seconds
    '''
    while time_sec:
        # The method takes two numbers and returns a pair of numbers consisting of their quotient and remainder.
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        # Overwrites the output for each iteration.
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1
        # Execute timer by enter a key -> TODO doesnt work with output timeformat

    print('Time Over! U did a great work!')


def work_timer():
    ''' User can set the time for his countdowntimer and run it.
    '''
    print(Fore.BLACK + Back.GREEN +
          'SET UR TIME AND PRESS ENTER                  ' + Style.RESET_ALL)
    sec = int(input('Time in Minutes: '))
    countdown(sec*60)
    # TODO Save workingtime on a special project - show sum of a project


# ------------------ Module functions ------------------


def get_modules():
    ''' Get just the modulnames without any other information.
    '''
    for i in modules:
        add_new_module_to_list(i[0])


def add_new_module_to_list(name):
    ''' Check if the given modul is in list, if not append to list

        Args:
            name (string) : name of the new modul/project
    '''
    try:
        modulenames.index(name)
    except:
        modulenames.append(name)


def add_new_modul():
    ''' Add a new modul/project, link(url) and linkdescription to ur database.
    '''
    print(Fore.BLACK + Back.GREEN +
          'ADD A NEW MODUL OR PROJECT                   ' + Style.RESET_ALL)

    print(modulenames)
    modul = input('Enter a new Modul- or Projectname: ')
    link = input('Paste a Link for this Modul: ')
    description = input('Linkdescription: ')
    add_new_module_to_list(modul)
    modules.append([modul, link, description])


def find_modul(search):
    ''' Shows all information about one searched modul.

        Args:
            search (string) : name of the searched modul/project
    '''
    searched_modul = []
    for i in range(len(modules)):
        if modules[i][0] == search:
            searched_modul.append([modules[i][1], modules[i][2]])

    print(search)
    print(tabulate(searched_modul, tablefmt='grid'))


def search_modul():
    ''' Search for a modul/project to show all information about it.
    '''
    searchedmodule = input('Enter a Modul or Project: ')
    try:
        modulenames.index(searchedmodule)
    except:
        print('The Modul ur looking for doesnt exist! \n')
    else:
        print('')
        print(Fore.BLACK + Back.GREEN +
              'Here are the information about {} !'.format(searchedmodule) + Style.RESET_ALL)
        # show just this one Module and all his Links
        find_modul(searchedmodule)


# ------------------ Calendar functions ------------------


def validate_time(time_string):
    ''' Validates a string representing a time

        Args: time_string (string) : string which should be a time
    '''
    try:
        # try to convert string to time format
        time_obj = datetime.strptime(time_string, '%H:%M')
    except ValueError:
        print('Incorrect time format, should be HH:MM')
        return False
    else:
        return True


def validate_date(date_string, date_format):
    ''' Validates a string representing a date

        Args:
            date_string (string) : string which should be a date

        Returns:
            date : date in datetime format
    '''
    try:
        # try to convert string to date format
        return datetime.strptime(date_string, date_format)
    except ValueError:
        print('Incorrect date format, should be DD/MM/YYYY')
        raise ValueError('Incorrect date format')


def get_appointments(start_date, end_date):
    ''' Finds all appointments between two dates.

        Args:
            start_date (date) : begin of the important period
            end_date (date) : end of the important period

        Returns:
            list: list with appointments in the given period
    '''
    interested_appointments = []

    for i in appointments:
        try:
            date_object = validate_date(i[0], '%Y-%m-%d')
        except:
            print('wrong date format')
        else:
            if start_date <= date_object.date() <= end_date:
                interested_appointments.append(i)

    return interested_appointments


def delete_old_appointments():
    ''' Deletes all passed appointments in the list.
    '''
    sort_appointments()
    for i in appointments:
        try:
            date_object = validate_date(i[0], '%Y-%m-%d')
        except:
            print('wrong date format')
        else:
            if today.date() > date_object.date():
                appointments.pop(appointments.index(i))


def sort_appointments():
    ''' Sorts the appointment list based on the days.
    '''
    appointments.sort(reverse=False, key=lambda x: x[0])


def show_days(day_appointments):
    ''' Shows the appointments per day.

        Args:
            day_appointments (list) : list with appointments grouped by day
    '''
    print(Fore.BLACK + Back.GREEN +
          'Appointments                                 ' + Style.RESET_ALL)
    appointments = []
    # if there are appointments in the list
    if any(day_appointments):
        # go through all days and appointments
        for i, day in enumerate(day_appointments):
            for j, appointment in enumerate(day):
                # get the date from the appointment group for the headline
                date_group = datetime.strptime(appointment[0], '%Y-%m-%d')
                # remove first column with the dates
                day_appointments[i][j].pop(0)
                # TODO mehrere kopien sind die alle nötig?
                # add new row to another list
                appointments.append(day_appointments[i][j])
            print(date_group.strftime('%d. %B %Y'))
            print(tabulate(appointments))
            print(' ')
            appointments.clear()
    else:
        print('No appointments')


def show_appointments():
    ''' Shows the appointments of today.
    '''
    # sort appointments from tho oldest to the newest
    sort_appointments()
    # use copy because of modification in the list should not effect the original one
    appointments_copy = deepcopy(appointments)
    appointments_grouped = []

    # Group by days
    for key, group in groupby(appointments_copy, key=lambda x: x[0]):
        # add group of one day
        appointments_grouped.append(list(group))
    # displays all appointments grouped by day
    show_days(appointments_grouped.copy())


def show_today():
    ''' Shows the appointments of today.
    '''
    appointments_today = []
    # gets all appointments with the date of today
    appointments_today.append(get_appointments(today.date(), today.date()))
    # displays all appointments grouped by day
    show_days(deepcopy(appointments_today))


def check_appointment(date_string):
    ''' Checks if there is an appointment on the given date string.

    Returns:
          bool: true if there is an appointment otherwise false
    '''
    check = False
    # go through the whole list
    for appointment in appointments:
        try:
            appointment.index(date_string)
        except:
            check = False
        else:
            return True

    return check


def get_month():
    ''' Gets the actual calendar list from calendar module.

        Returns:
             list: list with the calender view of the actual month
    '''
    year = datetime.today().year
    month = datetime.today().month

    return calendar.monthcalendar(year, month)


def show_month():
    ''' Shows the calendarview from the actual month wit marked days with appointments.
    '''
    print(Fore.BLACK + Back.GREEN +
          'Actual Month                                 ' + Style.RESET_ALL)
    # get month list
    month = get_month()
    # go through all days of the month
    for i, week in enumerate(month):
        for j, day in enumerate(week):
            # month is displayed week per week and if the first day is not
            # monday the missing days were filled with 0 also at the end of the month
            # remove all 0 and replace them
            if month[i][j] == 0:
                month[i][j] = ' '
            # if item is a real month day
            else:
                # create date string with the day item in the month
                day = str(today.year) + '-' + str(today.month).zfill(2) + \
                    '-' + str(month[i][j]).zfill(2)
                # check if date has an appointment
                is_appointment = check_appointment(day)
                # if date is today mark the item with grey background
                if (today - validate_date(day, '%Y-%m-%d')).days == 0:
                    # when addtional an appointment is on this day
                    if is_appointment:
                        month[i][j] = '\x1b[5;32;47m' + \
                            str(month[i][j]) + Style.RESET_ALL
                    else:
                        month[i][j] = '\x1b[0;30;47m' + \
                            str(month[i][j]) + Style.RESET_ALL
                # mark all dates with appointments with green text color
                elif is_appointment:
                    month[i][j] = Fore.GREEN + \
                        str(month[i][j]) + Style.RESET_ALL
    # TODO brauche ich die kopie wirklich?
    display_month = month.copy()

    # add headerline to list for the output
    display_month.insert(0, ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
    print(' ')
    print(today.strftime('%B'))
    print(tabulate(display_month, headers=('firstrow')))
    print(' ')


def add_appointment():
    ''' Adds an appointment to the list.
    '''
    print(Fore.BLACK + Back.GREEN +
          'Add appointment                              ' + Style.RESET_ALL)
    day = input('day (DD/MM/YYYY):')
    try:
        day = validate_date(day, '%d/%m/%Y')
    except:
        raise ValueError('wrong date format')

    time = input('time (hh:mm):')
    if not validate_time(time):
        raise ValueError('wrong time format')

    description = input('description:')
    appointments.append([str(day.date()), time, description])

# ------------------ List functions ------------------


def show_list_with_header(data_list, list_header):
    ''' prints all grades from the list.
    '''
    list_copy = deepcopy(data_list)
    list_copy.insert(0, list_header[0])
    print(tabulate(list_copy, headers=('firstrow')))

# ------------------ Grades functions ------------------


def add_grade():
    ''' Adds a grade to the grade list.
    '''
    print(Fore.BLACK + Back.GREEN +
          'Add Grade                                    ' + Style.RESET_ALL)
    semester = input('Semester:')
    module = input('Module:')
    # typüberprüfung!
    grade = input('Grade:')
    credits = input('Credits:')
    grades.append([semester, module, grade, credits])


def grades_average():
    ''' Calculates the grade point average and print it.
    '''
    print(Fore.BLACK + Back.GREEN +
          'Grades Average                               ' + Style.RESET_ALL)
    sum_products = 0
    sum_credits = 0
    for i in grades:
        sum_products = sum_products + float(i[2])*int(i[3])
        sum_credits = sum_credits + int(i[3])
    avg = sum_products/sum_credits
    average = [['grades average: ', str('{:.2f}'.format(avg))],
               ['total grades:', len(grades)],
               ['total credits:', sum_credits]]
    print(tabulate(average))


# ------------------ Main ------------------
fill_data()
while(True):
    print(Fore.BLACK + Back.GREEN +
          'Welcome to ur StudyOrganizer                 ' + Style.RESET_ALL)
    print_menu(menu_options)
    option = ''

    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')

    if option == 1:
        home()
    elif option == 2:
        module()
    elif option == 3:
        calendar_overview()
    elif option == 4:
        grades_overview()
    elif option == 5:
        save_data()
        print('Files were Saved')
        break
    else:
        print('Invalid option. Please enter a number between 1 and 5.')
