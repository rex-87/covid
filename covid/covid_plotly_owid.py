# -*- coding: utf-8 -*-
"""
	python38
	
	This project is an example of a Python project generated from cookiecutter-python.
"""

## -------- COMMAND LINE ARGUMENTS ---------------------------
## https://docs.python.org/3.7/howto/argparse.html
import argparse
CmdLineArgParser = argparse.ArgumentParser()
CmdLineArgParser.add_argument(
	"-v",
	"--verbose",
	help = "display debug messages in console",
	action = "store_true",
)
CmdLineArgs = CmdLineArgParser.parse_args()

## -------- LOGGING INITIALISATION ---------------------------
import misc
misc.MyLoggersObj.SetConsoleVerbosity(ConsoleVerbosity = {True : "DEBUG", False : "INFO"}[CmdLineArgs.verbose])
LOG, handle_retval_and_log = misc.CreateLogger(__name__)

try:
	
	## -------------------------------------------------------
	## THE MAIN PROGRAM STARTS HERE
	## -------------------------------------------------------	

	LOG.info("imports ...")
	import plotly.express as px
	import plotly.graph_objects as go
	import pandas as pd
	import requests
	import os
	import datetime

	# ---- raw csv to df
	owid_url = r'https://covid.ourworldindata.org/data/owid-covid-data.csv'
	today_str = datetime.datetime.now().strftime("%y%m%d")

	today_csv_path = today_str + '_owid.csv'
	if not os.path.exists(today_csv_path):
		LOG.info("get data from {} ...".format(owid_url))
		r = requests.get(owid_url)
		LOG.info("save data in {} ...".format(today_csv_path))
		with open(today_csv_path, 'w') as fout:
			fout.write(r.text)
	else:
		LOG.info("{} was already downloaded today.".format(owid_url))

	owid_df = pd.read_csv(today_csv_path)
	
	# column_name = 'total_cases'
	# column_name = 'new_cases'
	# column_name = 'total_deaths'
	# column_name = 'new_deaths'

	column_name_l = [
		'total_cases',
		'new_cases',
		'total_deaths',
		'new_deaths',
	]

	for column_name in column_name_l:

		# ---- create figure
		fig = go.Figure()	

		country_name_l = ['France', 'United Kingdom', 'Germany', 'Italy', 'Spain', 'Turkey', 'Israel', 'United States', 'Brazil', 'India', 'Russia']
		for country_name in country_name_l:
			df_ = owid_df[owid_df['location'] == country_name]
			# fig.add_trace(go.Scatter(x = df_['date'], y = df_[column_name]/, mode = 'markers', name = country_name))
			# fig.add_trace(go.Scatter(x = df_['date'], y = round(df_[column_name].rolling(7, center =True).sum()/7), mode = 'lines', name = '{} (7d)'.format(country_name)))
			fig.add_trace(go.Bar(
				x = df_['date'],
				y = round(1e8*df_[column_name]/df_['population']),
				# mode = 'markers',
				name = country_name,
				visible = 'legendonly',
			))
			fig.add_trace(go.Scatter(x = df_['date'], y = round(1e8*df_[column_name].rolling(7, center =True).sum()/7/df_['population']), mode = 'lines', name = '{} (7d)'.format(country_name)))
			# fig.add_trace(go.Scatter(x = df_['date'], y = round(1e8*df_[column_name].rolling(7, center =True).median()/df_['population']), mode = 'lines', name = '{} (7d)'.format(country_name)))

		# ---- update plot layout
		fig.update_layout(
			title = "Our World In Data: COVID-19 {} [per 100M]".format(column_name),
			xaxis=dict(
				type="date"
			),
			legend = dict(
				x=0.01,
				y=0.99,
			),
			margin = dict(
				l = 30,
				r = 10,
				b = 10,
				t = 50,
				pad = 4,
			),
		)
		
		fig.update_yaxes(automargin=True)

		# ---- show !
		fig.show()
	
	# fig.write_html("pfile.html", include_plotlyjs = 'cdn')
	
## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	# input("Press any key to exit ...")
	pass
