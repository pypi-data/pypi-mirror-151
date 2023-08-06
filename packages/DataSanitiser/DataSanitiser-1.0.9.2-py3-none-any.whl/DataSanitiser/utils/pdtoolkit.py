import re
import calendar
import numpy as np
import pandas as pd
from datetime import datetime


def calc_num_bus_days(start: datetime, end: datetime, holidays):
    """Calculate the number of business days between given start and end date

    Args:
        start (datetime): start time of a time range
        end (datetime): end time of a time range
        holidays (pd.Series): list of datetime elements or pandas data series
            of public holidays for exclusion

    Returns:
        int: number of business days

    """
    weekmask = 'Mon Tue Wed Thu Fri'

    bdr = pd.bdate_range(start=start, end=end, freq='C',
                         weekmask=weekmask, holidays=holidays)

    return len(bdr)


def check_wd(row):
    if pd.notna(row['Holiday Name']):
        return 'Public Holiday'
    elif row['Day_Name'] in ['Saturday', 'Sunday']:
        return 'Weekend'
    else:
        return 'Working Day'


def capitalise_name(name):
    name = name.strip()
    nl = name.split()
    nl = [n.capitalize() for n in nl]
    return ' '.join(nl)


def split_name(row, first_name=True):
    if pd.notnull(row['position']):
        sn = row['full_name'].split()
        if len(sn) >= 2:
            if first_name:
                return sn[0]
            else:
                return sn[-1]
        else:
            return ''
    else:
        return ''


def parse_date(string):
    p1 = r'\d{4}-\d{2}-\d{2}'
    p2 = r'\d{2}/\d{2}/\d{4}'
    c1 = re.findall(p1, string)
    c2 = re.findall(p2, string)
    if len(c1) > 0:
        p_string = c1[0]
        return datetime.strptime(p_string, r'%Y-%m-%d')
    elif len(c2) > 0:
        p_string = c2[0]
        try:
            return datetime.strptime(p_string, r'%d/%m/%Y')
        except:
            return datetime.strptime(p_string, r'%m/%d/%Y')
    elif string == 'nan':
        return np.nan
    else:
        return np.nan


def convert_to_timestamp(value):
    if pd.isnull(value):
        return np.nan
    else:
        return datetime.strftime(value, r'%Y-%m-%d %H:%M:%S')


def fix_inconsistency(df, exp_cols: list):
    act_cols = set(df.columns)
    add_cols = set(exp_cols) - set(exp_cols).intersection(act_cols)
    del_cols = act_cols - set(exp_cols).intersection(act_cols)
    for c in add_cols:
        df[c] = np.nan
    df.drop(columns=list(del_cols), inplace=True)
    df = df[exp_cols]
    return df


def check_cols_completeness(df, exp_cols):
    if (df.columns == exp_cols).sum() == df.shape[1]:
        return True
    else:
        return False


def get_month_range(year, month, out='start'):
    day_range = calendar.monthrange(year, month)
    if out == 'start':
        return datetime.datetime(year, month, 1)
    elif out == 'end':
        return datetime.datetime(year, month, day_range[1])
    else:
        return np.nan


def clean_id(x):
    try:
        return str(int(float(x)))
    except:
        return x


def check_dup_columns(df):
    cols = df.columns
    cols_lower = np.array([c.lower() for c in cols])
    unq, cnt = np.unique(cols_lower, return_counts=True)
    dup = unq[cnt > 1]
    # print(dup)

    dup = [c for c in cols if c.lower() in dup]
    print(f'Duplicated Columns: {dup}')


def parse_date(string):
    p1 = r'\d{4}-\d{2}-\d{2}'
    p2 = r'\d{2}/\d{2}/\d{4}'
    c1 = re.findall(p1, string)
    c2 = re.findall(p2, string)
    if len(c1) > 0:
        p_string = c1[0]
        return datetime.datetime.strptime(p_string, r'%Y-%m-%d')
    elif len(c2) > 0:
        p_string = c2[0]
        return datetime.datetime.strptime(p_string, r'%d/%m/%Y')
    elif string == 'nan':
        return np.nan
    else:
        print(string, type(string))
        raise IOError


def convert_to_timestamp(value):
    if pd.isnull(value):
        return np.nan
    else:
        return datetime.datetime.strftime(value, r'%Y-%m-%d %H:%M:%S')


def check_cols_completeness(df, exp_cols):
    if (df.columns == exp_cols).sum() == df.shape[1]:
        return True
    else:
        return False
