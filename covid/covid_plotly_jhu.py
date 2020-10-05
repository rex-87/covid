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

    # ---- raw csv to df
    LOG.info("get data from https://github.com/CSSEGISandData/COVID-19 ...")
    confir_df = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv').transpose().reset_index()
    deaths_df = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv').transpose().reset_index()

    # ---- create date column from index
    LOG.info("create date column from index ...")
    cumul_confir_df = confir_df.loc[4:,:].rename(columns={'index':'date'})
    cumul_deaths_df = deaths_df.loc[4:,:].rename(columns={'index':'date'})

    # ---- use appropriate date format for plotly
    LOG.info("use appropriate date format for plotly ...")
    cumul_confir_df.date = pd.to_datetime(cumul_confir_df.date)    
    cumul_deaths_df.date = pd.to_datetime(cumul_deaths_df.date)    

    # ---- rename columns with country names
    LOG.info("rename columns with country names ...")    
    for c in range(266):
        cumul_confir_df = cumul_confir_df.rename(columns={c:"{}; {}".format(confir_df.loc[1, c], confir_df.loc[0, c]).replace('; nan', '')})
        cumul_deaths_df = cumul_deaths_df.rename(columns={c:"{}; {}".format(deaths_df.loc[1, c], deaths_df.loc[0, c]).replace('; nan', '')})

    # ---- daily processing
    LOG.info("process cumul data to get daily data ...")  
    daily_confir_df = pd.DataFrame()
    daily_deaths_df = pd.DataFrame()
    daily_confir_df['date'] = cumul_confir_df.loc[:, 'date']
    daily_deaths_df['date'] = cumul_deaths_df.loc[:, 'date']
    for c in range(1, 266):
        
        # ---- confirmed cases
        daily_confir_df[cumul_confir_df.columns[c]] = cumul_confir_df[cumul_confir_df.columns[c]].diff()
        cumul_confir_df[cumul_confir_df.columns[c]+' (7day)'] = round(cumul_confir_df[cumul_confir_df.columns[c]].rolling(7, center =True).sum()/7)
        daily_confir_df[cumul_confir_df.columns[c]+' (7day)'] = round(daily_confir_df[cumul_confir_df.columns[c]].rolling(7, center =True).sum()/7)        
        
        # ---- deaths
        daily_deaths_df[cumul_deaths_df.columns[c]] = cumul_deaths_df[cumul_deaths_df.columns[c]].diff()
        cumul_deaths_df[cumul_deaths_df.columns[c]+' (7day)'] = round(cumul_deaths_df[cumul_deaths_df.columns[c]].rolling(7, center =True).sum()/7)
        daily_deaths_df[cumul_deaths_df.columns[c]+' (7day)'] = round(daily_deaths_df[cumul_deaths_df.columns[c]].rolling(7, center =True).sum()/7)

    # ------------------
    # DISPLAY PLOTS
    # ------------------
    LOG.info("plot ...")    
   
    
    # ---- parameters
    country_name_l = ['France', 'United Kingdom', 'Germany', 'Italy', 'Spain', 'Belgium', 'Sweden', 'Netherlands',]
    # country_name_l = ['US', 'Brazil', 'India', 'Russia']
    
    l = [ 
        [cumul_confir_df, 'cumul confirmed'],
        [daily_confir_df, 'daily confirmed'],
        [cumul_deaths_df, 'cumul deaths'],
        [daily_deaths_df, 'daily deaths'],
    ]

    # to_plot_df, txt = cumul_confir_df, 'cumul confirmed'
    # to_plot_df, txt = daily_confir_df, 'daily confirmed'
    # to_plot_df, txt = cumul_deaths_df, 'cumul deaths'
    # to_plot_df, txt = daily_deaths_df, 'daily deaths'
    
    for to_plot_df, txt in l:

        # ---- create figure
        fig = go.Figure()
        
        # ---- prepare plots
        for country_name in country_name_l:
           
           # ---- unfiltered
            fig.add_trace(
                go.Bar(
                    x = to_plot_df['date'],
                    y = to_plot_df[country_name],
                    # mode = 'markers',
                    name = country_name,
                    visible = 'legendonly',
                )
            )
          
            # ---- filtered
            fig.add_trace(
                go.Scatter(
                    x = to_plot_df['date'],
                    y = to_plot_df[country_name+' (7day)'],
                    mode = 'lines',
                    name = country_name+' (7d)',
                )
            )
        
        # ---- time slider
        fig.update_layout(
            title = "COVID-19: "+txt,
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

        # show !
        fig.show()
    
    # import IPython; IPython.embed(colors='Neutral')

## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	# input("Press any key to exit ...")
    pass
