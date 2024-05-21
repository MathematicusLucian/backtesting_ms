import sys
import os
from datetime import datetime
import pytz
# from botasaurus import bt
import json
import re
import urllib
import datetime
from datetime import datetime
# from langdetect import detect
# from langdetect.lang_detect_exception import LangDetectException
from itertools import groupby
import pathlib
import os
import pandas as pd
from dotenv import main
main.load_dotenv(main.find_dotenv())
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import talib as ta  
# CWD_DIR = os.getcwd()
# BASE_DIR = os.path.abspath(os.path.join(CWD_DIR, 'src'))
# load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

def add_indicators(data):
    data["RSI"] = ta.rsi(data["Close"])
    data["EMA"] = ta.EMA(data["Close"])
    data["WMA"] = ta.WMA(data["Close"])
    data["ROC"] = ta.ROC(data["Close"])
    data["TEMA"] = ta.TEMA(data["Close"])
    data["CMO"] = ta.CMO(data["Close"])
    data["SAR"] = ta.SAR(data["High"],data["Low"])
    data["WILLR"] = ta.WILLR(data["High"],data["Low"],data["Close"],timeperiod = 15)
    data["CCI"] = ta.CCI(data["High"],data["Low"],data["Close"],timeperiod = 15)
    data["PPO"] = ta.PPO(data["Close"],fastperiod = 6,slowperiod = 15)
    data["MACD"] = ta.MACD(data["Close"],fastperiod = 6,slowperiod = 15)[0]
    a = ta.WMA(data["Close"],timeperiod = 15//2)
    b = data["WMA"]
    data["HMA"] = ta.WMA(2*a - b,timeperiod = int(15**(0.5)))
    data["ADX"] = ta.ADX(data["High"],data["Low"],data["Close"],timeperiod = 15)
    data.dropna(inplace = True)
    data.set_index("Date",inplace = True)  

def retrieve_chained_header_item(df, first_key, second_key):
    return df[:, (first_key, second_key)]

def is_arg(arg_str: str) -> bool:
    for i, arg in enumerate(sys.argv):
        if arg==arg_str: 
            return True
    return False

def get_envar(envar_name: str) -> str:
    return os.environ.get(envar_name)

def get_root_dir():
    return os.path.abspath(os.curdir)

def get_datetime_now(format=None):
    if format == "timestamp":
        return datetime.now().timestamp()
    elif format == "iso":
        today = datetime.now()
        iso_date = today.isoformat()
        iso_date_with_hash = datetime.now().isoformat('#')
        iso_date_with_space = today.isoformat()
        today_datestring = datetime.today()
        aware_us_central = datetime.now(pytz.timezone('US/Central'))
        iso_date = aware_us_central.isoformat()
    else:
        return datetime.now()

# def get_search_url(site_name, site_data):
#     if(site_name=="LinkedIn"):
#         search_url = get_env_var('LINKEDIN_SEARCH_URL') #https://reqbin.com/
#     else:
#         search_url = field_from_list_elnone("search_url", site_data)
#     return search_url

# def add_kwarg_vars_to_url(kwargs_str, kwarg_var_name, search__role_title, kwargs, page_num, start):
#     if(kwarg_var_name=="job_title"):
#         kwarg_var_value = search__role_title
#     elif(kwarg_var_name=="position"):
#         kwarg_var_value = str(1)
#     elif(kwarg_var_name=="page_num"):
#         kwarg_var_value = page_num
#     elif(kwarg_var_name=="start"):
#         kwarg_var_value = start
#     else:
#         kwarg_var_value = field_from_list_elnone(kwarg_var_name, kwargs)

#     return add_variables_to_str(kwargs_str, kwarg_var_name, kwarg_var_value)
    
# def build_kwargs_string(kwargs_str, site_name, search__role_title, kwargs, page_num, start):    
#     regex_pattern = "{([^{]*?)}" 

#     for kwarg_var_name in re.findall(regex_pattern, kwargs_str):
#         kwargs_str = add_kwarg_vars_to_url(kwargs_str, kwarg_var_name, search__role_title, kwargs, page_num, start)

#     return kwargs_str

# def get_url_and_kwargs(site_name, site_data):
#     if(site_name=="LinkedIn"):
#         search_url = get_env_var('LINKEDIN_SEARCH_URL') #https://reqbin.com/
#         kwargs_str = get_env_var('LINKEDIN_KWARGS_STR')
#     else:
#         search_url = field_from_list_elnone("search_url", site_data)
#         kwargs_str = field_from_list_elnone("kwargs_str", site_data)
#     return search_url, kwargs_str

def add_variables_to_str(str_to_update, var_name, var_value): 
    if(isinstance(var_value, str) or type(var_value) != "str"):
        var_value = str(var_value)

    field_to_replace = "{"+ var_name+"}"
    str_to_update = str_to_update.replace(field_to_replace,var_value)

    return str_to_update

def is_field_in_list(field, list):
    return field in list

def field_from_list_elnone(field, list):
    return list[field] if is_field_in_list(field,list) else None

def is_field_in_list_set_to_value(field, list, value):
    return is_field_in_list(field, list) and field_from_list_elnone(field, list)==value

# def get_list_of_matching_items(page, selector: str, wait=Wait.SHORT):
#     # try:
#     els = page.get_elements_or_none_by_selector(selector, wait)

#     if els is None:
#         return None
#     return els
#     # except StaleElementReferenceException:
#     #     return page.text(selector,wait)

def extract_text(el):
    return el.text.strip()

def extract_texts(list_of_elements):
    return list(map(extract_text, list_of_elements))

def get_texts(list_of_elements):
    texts = extract_texts(list_of_elements)
    return texts

def extract_html(el):
    return el.get_attribute("innerHTML")

def extract_htmls(list_of_elements):
    x = list(map(extract_html, list_of_elements))
    return x

def get_htmls(list_of_elements):
    htmls = extract_htmls(list_of_elements)
    return htmls

def get_json_file(file_name):
    with open(file_name) as user_file:
        # launch_tasks(*tasks_to_be_run)
        # https://github.com/omkarcloud/web-scraping-template/tree/master
        sites_data = user_file.read()
        sites_data_json = json.loads(sites_data)
        user_file.close()
        return sites_data_json

# def safe_detect(text):
#     try:
#         return detect(text)
#     except LangDetectException:
#         return 'en'

def string_to_delta(string_delta):
    value, unit, _ = string_delta.split()
    return datetime.timedelta(**{unit: float(value)})

def parse_regex(val):
    if isinstance(val, str):
        return re.compile(val)
    return val

def filter_pair(list_to_filter, key_to_filter_by, key_to_return):
    for x in list_to_filter:
        if x["name"] == key_to_filter_by:
            return x[key_to_return]

# def remove_duplicates(joblist, config):
#     # If two jobs have the same title and company.
#     joblist.sort(key=lambda x: (x['title'], x['company']))
#     joblist = [next(g) for k, g in groupby(joblist, key=lambda x: (x['title'], x['company']))]
#     return joblist

def save_dataframe(df: pd.DataFrame):
    df.to_csv('../database/scraped.csv', index=False, encoding='utf-8')
    df.to_excel('../database/scraped.xlsx', index=False)

# def write_output(data, result):
#     bt.write_json(result, data)
#     bt.write_csv(result, data)

def fetch_currency_archive_data(currency):
    return pd.read_csv(f"{get_root_dir()}/backtesting_data/crypto_archive/{currency}.csv")

def create_plotly(df):
    fig = go.Figure(data=[go.Candlestick(x=df.date,
                open=df.open,
                high=df.high,
                low=df.low,
                close=df.close)])
    fig.show()

def get_min_date(df):
 return df.date.min()

def get_max_date(df):
 return df.date.max()

def get_range_for_number_of_days(df, days):
   return df.tail(days)

def get_range_between_dates(df, date_from, date_to):
   return df.loc[date_from:date_to]

def get_historic_data(currency, date_from, date_to):
    df = fetch_currency_archive_data(currency)
    return get_range_between_dates(df, date_from, date_to)

# start = datetime(2022,1,1)
# end = datetime(2024,1,1)
# data = pdr.DataReader("TSLA","yahoo")
# data.to_csv("data/stock_data.csv")