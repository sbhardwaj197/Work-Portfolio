#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: salonibhardwaj

Collaborated with: Muskaan Aggarwal, Arunima Mehrotra

"""


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import geopandas

from geopandas import GeoDataFrame

from shiny import reactive, App, render, ui

#data & shapefile read & loading 

path = r'/Users/salonibhardwaj/Desktop/DAP_2_labs/Homeworks_2.0/homework-4-salonibhardwaj'

cta_shp = os.path.join(path, 'CTA_RailLines', 'CTA_RailLines.shp')

com_shp = os.path.join(path, 'Comm_20Areas__1_', 'CommAreas.shp')

df_cta = geopandas.read_file(cta_shp)

df_com = geopandas.read_file(com_shp)

logo_url = 'https://design.chicago.gov/assets/img/logo/LOGO-CHICAGO-horizontal.png'

options = ['CCVI Score', 'Cumulative Deaths 2006 - 2010' ]

yn = ['Yes', 'No']

# Cleaning CTA rail lines
#source: Class lecture files from spatial data week

def get_col(l):
    if 'Blue' in l:
        return 'b'
    elif 'Red' in l:
        return 'r'
    elif 'Purple' in l:
        return 'purple'
    elif 'Brown' in l:
        return 'brown'
    elif 'Yellow' in l:
        return 'yellow'
    elif 'Green' in l:
        return 'green'
    elif 'Pink' in l:
        return 'pink'
    elif 'Orange' in l:
        return 'orange'
    
color_dict = {l:get_col(l) for l in df_cta['LINES'].unique()}

# Data cleaning & manipulation to drop unecessary columns 

chi_covid = pd.read_csv(os.path.join(path, 'Chicago_COVID-19_Community_Vulnerability_Index__CCVI_.csv'))
chi_covid = chi_covid.iloc[:,0:4]
chi_covid = chi_covid.dropna()
chi_covid = chi_covid.reset_index()

chi_ph = pd.read_csv(os.path.join(path, 'Public_Health_Statistics_-_Selected_underlying_causes_of_death_in_Chicago__2006_2010_-_Historical.csv'))
chi_ph = chi_ph.loc[chi_ph['Cause of Death'] == 'All Causes']
chi_ph = chi_ph.iloc[:,0:4]

chi_stats = pd.merge(chi_covid, chi_ph, how='outer', on='Community Area Name') 
chi_stats = chi_stats.drop(labels=['index','Geography Type','Community Area or ZIP Code','Cause of Death', 'Community Area' ], axis=1)  # eliminating insignificant columns
chi_stats = chi_stats.dropna()

df_com['COMMUNITY'] = df_com['COMMUNITY'].str.title()

gis_chi_stats = pd.merge(chi_stats, df_com, how='outer', left_on='Community Area Name', right_on='COMMUNITY')

gis_chi_stats = GeoDataFrame(gis_chi_stats) 

#shiny app

app_ui = ui.page_fluid(
    ui.row(
        ui.column(4, ui.img(src=logo_url, height=100, width=288)),
        ui.column(8, ui.h1('City of Chicago Public Health Statistics'), ui.hr())
        
    ),
    ui.row(
        ui.column(2, ui.input_select(id='para', 
                                     label='Choose a parameter',
                                     choices=(options))),
        ui.column(2, ui.input_select(id='trains', 
                                     label='Display Trains',
                                     choices=(yn))),
       ui.column(8, ui.output_plot('choropleth')),
    ), 
    
    ui.row(
        ui.column(12, ui.h6(' * CCVI - Covid Community Vulnerability Index' , align = 'center')))
)



def server(input, output, session):
 
    @output
    @render.plot
    def choropleth():
        fig, ax = plt.subplots(figsize=(8,8))
    
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.1)
    
        ax = gis_chi_stats.plot(ax=ax, column=input.para(), legend=True, cax=cax, edgecolor='black', cmap="OrRd")
        ax.axis('off')
        ax.set_title(f'{input.para()} in Chicago Community Areas')
        # toggle for trains
        if (input.trains()=='Yes'):
            df_com.plot(ax=ax, alpha=0, color = 'white' , edgecolor='white', label='Community Areas')
            for line in df_cta['LINES'].unique():
                    c = color_dict[line]
                    df_cta[df_cta['LINES'] == line].plot(ax=ax, color=c, alpha=1, linewidth=1)
                    
   
app = App(app_ui, server)





