from os.path import dirname, join
import re

MAIN_DIRECTORY = dirname(dirname(__file__))
def full_path(*path):
    return join(MAIN_DIRECTORY, *path)

def assign_code(record, k, location, area):
    first_name = record['firstname']
    first_name = ''.join(c for c in first_name if c.isalnum())
    first_name = first_name[0:1]
    last_name = record['lastname']
    last_name = ''.join(c for c in last_name if c.isalnum())
    last_name = last_name[0:4]
    jury_num = k
    room_code = rooms_dict[location]
    area_code = area[0:3]
    return (first_name.lower() +
            last_name.lower() +
            str(jury_num) +
            '-'+ room_code + area_code)

def intersection(a, b, c, d):
    return list(set(a) & set(b) & set(c) & set(d))

def search_records(target_sheet, record):
    for key, value in record:
        if key == 'firstname':
            fn_temp = target_sheet.findall(value)
            fn = [i.row for i in fn_temp]
        if key == 'lastname':
            ln_temp = target_sheet.findall(value)
            ln = [i.row for i in ln_temp]
        if key == 'date':
            d_temp = target_sheet.findall(value)
            d = [i.row for i in d_temp]
        if key == 'time':
            t_temp = target_sheet.findall(value)
            t = [i.row for i in t_temp]
        return intersection(fn, ln, d, t)

def zeropad_int_pairs(string):
    """
    Takes a string and pads any instance of a single integer with a prepended
    zero so that all integers come in at least pairs
    """
    counter = 0
    prev_int = False #Indicator if previous character is an int
    go_to_end = False
    for c in string:
        current_int = str.isdigit(c) #Indicator if current character is an int
        if prev_int and current_int: #Case where ints are already in pairs
            prev_int = False
            current_int = False
            go_to_end = True
        if current_int and not prev_int: #Case where this is the first int
            prev_int = True
        if prev_int and not current_int and not go_to_end: #Case where first int was last int
            string = string[:counter-1] + '0' + string[counter-1:]
            counter += 1 #To account for the additional character added
            prev_int = False
            current_int = False
        counter += 1 #Iterate the counter
    string = remove_ordinals(string) #Remove Ordinal Suffixes
    return string

def remove_ordinals(string):
    """
    Remove ordinal suffixes from a string
    """
    return re.sub(r"(?<=[0-9])(?:st|nd|rd|th)", '', string)

rooms_dict = {
    'Salmon Recital Hall, Bertea Hall 100': '0',
    'Crean Hall Recital Hall, Oliphant Hall 103': '1',
    'Bertea Hall 121': '2'
}

