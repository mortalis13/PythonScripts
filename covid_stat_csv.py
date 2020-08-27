# Show statistics on COVID-19 spread and build a chart
# Uses the 'countries' list as input data (change/add country names and number of last values to show in chart)
# Data Source: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

import json, csv, requests, codecs, os
from datetime import datetime
from io import StringIO
from io import BytesIO
import xlsxwriter


# todo: US
countries = [
  ['France', 80],
  ['Spain', 80],
  ['Italy', 80],
  ['Germany', 80],
  ['Ukraine', 80],
  ['Russia', 80],
]


class Values:
  CONFIRMED_LABEL = 'confirmed'
  DEATHS_LABEL = 'deaths'
  RECOVERED_LABEL = 'recovered'
  
  DATE_FORMAT_STR = '%y/%m/%d'
  
  data_xls_path = '_files/cov-data.xlsx'
  
  url_str_confirm = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
  url_str_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
  url_str_recover = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'


def generate_next_filename(filepath, pat=None):
  if pat:
    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    name,ext = os.path.splitext(file_name)
    
    name_check = regex_search(name, '^(.+?)' + pat + '\d+$', 1)
    if name_check:
      filepath = file_dir + '/' + name_check + ext
  
  res_filepath = filepath
  file_exists = os.path.exists(filepath)

  counter = 2
  
  while file_exists:
    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    name,ext = os.path.splitext(file_name)
    file_name = name + '_' + str(counter) + ext
    counter += 1
    
    res_filepath = file_dir + '/' + file_name
    file_exists = os.path.exists(res_filepath)

  return res_filepath


def get_data(url_str, country):
  print('== get_data(): [{}] "{}"\n'.format(country, url_str))

  r = requests.get(url_str)
  content = r.content
  content = content.decode()
  # print(content)
  f = StringIO(content)
  
  cin = csv.DictReader(f)
  print(cin.fieldnames)
  print()
    
# ----------
  for row in cin:
    if row['Country/Region'] == country and row['Province/State'] == '':
      print(row, '\n')
      i = 0
      his = {}
      
      for item in row:
        # print('{}: {}'.format(item, row[item]))
        if i > 3:
          date_parts = item.split('/')
          date_parts = ['{:02d}'.format(int(p)) for p in date_parts]
          # yy/mm/dd
          h_date = '{}/{}/{}'.format(date_parts[2], date_parts[0], date_parts[1])
          his[h_date] = row[item]
        i += 1
      
      return his

def build_xls(country, num_values, workbook):
# ---------- Get data
  his_confirm = get_data(Values.url_str_confirm, country)
  his_death   = get_data(Values.url_str_death, country)
  his_recover = get_data(Values.url_str_recover, country)
  
  total_rows = len(his_confirm)
  num_values = min(num_values, total_rows)
  
# ---------- Prepare XLS
  sheet_name = country
  worksheet = workbook.add_worksheet(sheet_name)
  
  date_format = workbook.add_format({'num_format': 'yy/mm/dd'})
  header_format = workbook.add_format({'bold': True, 'align': 'center'})
  
  worksheet.set_row(0, None, header_format)
  
# ---------- Write data table (reverse order, sorted by date desc)
  xr = 1
  xc = 0
  worksheet.write(0, xc, 'date')
  worksheet.write(0, xc+1, Values.CONFIRMED_LABEL)
  for k in sorted(his_confirm, reverse=True):
    date_str = datetime.strptime(k, Values.DATE_FORMAT_STR)
    worksheet.write_datetime(xr, xc, date_str, date_format)
    worksheet.write_number(xr, xc+1, int(his_confirm[k]))
    xr += 1
    
  xr = 1
  xc = 2
  worksheet.write(0, xc, Values.DEATHS_LABEL)
  for k in sorted(his_death, reverse=True):
    date_str = datetime.strptime(k, Values.DATE_FORMAT_STR)
    worksheet.write_number(xr, xc, int(his_death[k]))
    xr += 1
    
  xr = 1
  xc = 3
  worksheet.write(0, xc, Values.RECOVERED_LABEL)
  for k in sorted(his_recover, reverse=True):
    date_str = datetime.strptime(k, Values.DATE_FORMAT_STR)
    worksheet.write_number(xr, xc, int(his_recover[k]))
    xr += 1
    
# ---------- Post formatting
  worksheet.set_column(xc+1, xc+1, 4, None)
  
# ---------- Plot the chart
  xc = 0
  chart = workbook.add_chart({'type': 'line'})
  chart.add_series({
    'name':        Values.CONFIRMED_LABEL.title(),
    'categories':  [sheet_name, 1, xc, num_values, xc],
    'values':      [sheet_name, 1, xc+1, num_values, xc+1],
    'line':        {'width': 3, 'color': '#4a7ebb', 'transparency': 30},
    # 'data_labels': {'value': True, 'position': 'above', 'font': {'name': 'Consolas', 'size': 14, 'bold': True}},
  })
  
  chart.add_series({
    'name':        Values.RECOVERED_LABEL.title(),
    'categories':  [sheet_name, 1, xc, num_values, xc],
    'values':      [sheet_name, 1, xc+3, num_values, xc+3],
    'line':        {'width': 3, 'color': '#48d75e', 'transparency': 30},
  })
  
  chart.add_series({
    'name':        Values.DEATHS_LABEL.title(),
    'categories':  [sheet_name, 1, xc, num_values, xc],
    'values':      [sheet_name, 1, xc+2, num_values, xc+2],
    'line':        {'width': 3, 'color': '#555555', 'transparency': 30},
  })
  
  chart.set_x_axis({
    'date_axis': True,
    'num_font': {'size': 12, 'bold': False, 'rotation': -50},
    'num_format': 'dd/mm',
    'major_unit': 3,
    'major_unit_type': 'days',
    'major_gridlines': {'visible': True, 'line': {'color': '#aaaaaa'}}
  })
  chart.set_y_axis({
    'display_units': 'thousands',
    'display_units_visible': True,
    'major_gridlines': {'visible': True, 'line': {'color': '#cccccc'}}
  })
  
  # chart.set_drop_lines()
  # chart.set_legend({'none': True})
  
  worksheet.insert_chart(0, xc+5, chart, {'x_scale': 2.8, 'y_scale': 2.4})


def run():
  print('==covid_stat_csv\n')
  global countries
  
  data_xls_path = generate_next_filename(Values.data_xls_path)
  workbook = xlsxwriter.Workbook(data_xls_path)
  
  for data in countries:
    build_xls(data[0], data[1], workbook)
  
  workbook.close()
  
  print('data_xls_path: "{}"'.format(data_xls_path))


# -----
run()
