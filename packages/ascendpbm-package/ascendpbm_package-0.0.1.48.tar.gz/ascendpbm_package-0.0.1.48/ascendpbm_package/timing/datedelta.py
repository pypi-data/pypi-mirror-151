import datetime

def monthdelta(months=0,operation='add',date=None):
    """Adds or removes the specified from number of months from a given date.
    It will leave the day of the month intact unless it is outside the end of the month (29,30,31)"""
    if date == None:
        date = datetime.datetime.now()
    if operation == 'add':
        newmonth = date.month + months
        def correct_month_year_add(year, newmonth):
            newyear = year
            if newmonth > 12:
                newmonth = newmonth - 12
                newyear = newyear + 1
                newyear, newmonth = correct_month_year_add(newyear, newmonth)
            return (newyear, newmonth)
        newyear, newmonth = correct_month_year_add(date.year, newmonth)
    if operation == 'subtract':
        newmonth = date.month - months
        def correct_month_year_sub(year, newmonth):
            newyear = year
            if newmonth <= 0:
                newmonth = 12 + newmonth
                newyear = newyear - 1
                newyear, newmonth = correct_month_year_sub(newyear, newmonth)
            return (newyear, newmonth)
        newyear, newmonth = correct_month_year_sub(date.year, newmonth)
    try:
        newdate = datetime.datetime(year=newyear, month=newmonth, day=date.day)
    except ValueError as e:
        end_of_months = [31,30,29,28]
        if str(e) == 'day is out of range for month':
            for day in end_of_months:
                try:
                    newdate = datetime.datetime(year=newyear, month=newmonth, day=day)
                    break
                except:
                    continue
    return newdate