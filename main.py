import calendar
import datetime
import ephem
import pandas as pd
import os


Y = 2024


def get_moon_phase(date: datetime.date) -> float:
    """
    Give the moon phase on a given day and returns the number day after the new moon.
    
    Parameters:
        date (datetime.date): date of the moon phase
        
    Returns:
        day_after_new_moon (float): number day after the new moon
    """
    synodic_month = 29.530588853

    date = ephem.Date(date)

    next_new_moon = ephem.next_new_moon(date)
    previous_new_moon = ephem.previous_new_moon(date)

    day_after_new_moon = ((date - previous_new_moon) / (next_new_moon - previous_new_moon)) * synodic_month

    return day_after_new_moon

def create_calendar(Y: int) -> pd.DataFrame:
    """
    Create a calendar for a given year.

    Parameters:
        Y (int): year of the calendar
        
    Returns:
        dates (pd.DataFrame): calendar of the year
    """
    months = [M for M in range(1, 13)]
    dates = pd.DataFrame(columns = months)

    for M in months:
        max_month_day = calendar.monthrange(Y, M)[1]
        for d in range(1, max_month_day + 1):
            date = datetime.date(Y, M, d)
            day_name_number = calendar.weekday(Y, M, d)
            day_name_string = calendar.day_abbr[day_name_number]
            lunation = get_moon_phase(date)

            dates.at[d, M] = [date, day_name_string, lunation]
    
    return dates

dates = create_calendar(Y)

day_row = '\\begin{tabular}{cccccccccccccc} \n'

for M in dates.columns:
    day_row = day_row + '\t& \Huge{%s}' % (calendar.month_name[M])

day_row = day_row + '\\\\'
day_row = day_row + ' &&&&&&&&&&&& \\\\ \n'

calc = '\\begin{tabular}{cccccccccccccc} \n'

for d in dates.index:
    for M in dates.columns:
        
        if str(dates[M][d]) == 'nan':
            day_row = day_row + '\t& '
            calc = calc + '\t& '

        else:
            lunation = dates[M][d][2]
            day_name = dates[M][d][1]

            if M == 1:
                day_row = day_row + '\t \\numberDay{%i}' % (d) + ' & \moon[scale=\moonsize, sky colour=\skycolour]{%f}{%s} &' % (lunation, day_name)
                calc = calc + '\t %i.' % (d) + ' & %i-%i-%i' % (Y,M,d) + ' &'
            elif M == 12:
                day_row = day_row + '\t \moon[scale=\moonsize, sky colour=\skycolour]{%f}{%s} \t & \\numberDay{%i} \\\\ \n' % (lunation, day_name, d)
                calc = calc + '\t & %i.' % (d) + '\\\\ \n'
            else:
                day_row = day_row + '\t \moon[scale=\moonsize, sky colour=\skycolour]{%f}{%s} &' % (lunation, day_name)
                calc = calc + '\t %i-%i-%i' % (Y,M,d) + ' &'


day_row = day_row + '\end{tabular} \n \\vspace{2em}'

with open('body.tex','w', encoding="utf-8") as file:
    file.write(day_row)
    file.close()

os.system('pdflatex Luna_calendar_tex_header.tex')