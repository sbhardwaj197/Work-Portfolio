import pandas as pd
import datetime

import os
import numpy as np

import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
import geopandas as gpd
import re 
from shiny import App, render, ui, reactive
from shiny import *
from shiny.types import ImgData
import seaborn as sns
import us


# to run, open anaconda terminal and write the following:
# shiny run --reload /Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/shinyplotting.py

# =========================================================================================================
    
#                                         PLOTTING ON SHINY 

# =========================================================================================================
#                                    DATA CLEANING AND MANIPULATION 
# =========================================================================================================


base_path = r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Data'
pew_path = os.path.join(base_path, 'Wage Gap by Metropolitan Area Detailed Tables - Wage Gap by Metro Area Detailed Table.csv')
msa_path = os.path.join(base_path, 'tl_2019_us_cbsa', 'tl_2019_us_cbsa.shp')
msa = gpd.read_file(msa_path)
msa = msa[['GEOID', 'geometry']]
msa["GEOID"] = pd.to_numeric(msa["GEOID"])

# =========================================================================================================
## Women’s wages as a % of men’s wages, MSA level 
# =========================================================================================================

pew_perc = pd.read_csv(pew_path, skiprows=11)

# selecting spcific columsn which represent women's wages as percentage of men's wages
pattern = ['dollars', 'rank', 'change']
for p in pattern: 
    drop_lst = [col for col in (pew_perc.columns) if col.find(p)>-1]
    pew_perc = pew_perc.drop(drop_lst, axis=1)

pew_perc['MSA'], pew_perc['state'] = pew_perc['MSA'].str.split(',', 1).str

# removing all unnecessary characters from the dataframe so as to convert it into numeric 
for col in pew_perc:
    pew_perc[col] = pew_perc[col].str.replace('$', '')
    pew_perc[col] = pew_perc[col].str.replace(',', '')
    pew_perc[col] = pew_perc[col].str.replace('%', '')
    pew_perc[col][pew_perc[col] == 'no data'] = None 
    
pew_perc.drop(pew_perc.tail(1).index,inplace=True)

numeric_col = list(pew_perc.columns)
numeric_col = numeric_col[-1:] + numeric_col[:-1]
pew_perc = pew_perc[numeric_col]
numeric_col = numeric_col[2:] 
for col in numeric_col:
    pew_perc[col] = pew_perc[col].astype(float)

# convert from wide to long format
pew_perc_clean = pd.melt(pew_perc, id_vars = ['state', 'MSA', 'FIPS'], value_vars=[
    '16+_2019_metro_perc', '16+_2000_metro_perc', '16_29_2019_metro_perc', 
    '16_29_2000_metro_perc', '30_49_2019_metro_perc', '30_49_2000_metro_perc', 
    '50+_2019_metro_perc', '50+_2000_metro_perc'])
pew_perc_clean.rename(columns={'value':'percentage'}, inplace=True)

# cleaning up the dataframe to represent one individual entry as a spcific age-year-MSA combination
pew_perc_clean['age'], pew_perc_clean['yearval'] = pew_perc_clean['variable'].str.split('_', 1).str
pew_perc_clean = pew_perc_clean.drop('variable', axis=1)
pew_perc_clean['age'] = pew_perc_clean['age'].apply(lambda x: '16-29' if  x == '16' else x)
pew_perc_clean['age'] = pew_perc_clean['age'].apply(lambda x: '30-49' if  x == '30' else x)
pew_perc_clean['age'] = pew_perc_clean.age.astype('category')

pew_perc_clean['year'] = pew_perc_clean['yearval'].str.extract('(20.*)')[0].str[:-11]
pew_perc_clean["year"] = pd.to_numeric(pew_perc_clean["year"])
pew_perc_clean = pew_perc_clean.drop('yearval', axis=1)

pew_perc_clean = pew_perc_clean[['FIPS', 'MSA', 'state', 'age', 'year', 'percentage']]

# convert dataframe into geopandas so as to plot women's wages as a percentage of men's wages
pew_perc_final = pew_perc_clean.merge(msa, left_on='FIPS', right_on='GEOID', how = 'inner')
pew_perc_final = pew_perc_final.drop('GEOID', axis=1)

pew_perc_final = gpd.GeoDataFrame(pew_perc_final)

# =========================================================================================================
## Median annual women’s earnings and men’s earnings
# =========================================================================================================

pew_earn = pd.read_csv(pew_path, skiprows=11)

# selecting spcific columsn which represent median annual earnings for men and women 
pattern2 = [ 'rank', 'change', 'perc']
for p in pattern2: 
    drop_lst2 = [col for col in (pew_earn.columns) if col.find(p)>-1]
    pew_earn = pew_earn.drop(drop_lst2, axis=1)
    
pew_earn['MSA'], pew_earn['state'] = pew_earn['MSA'].str.split(',', 1).str

# removing all unnecessary characters from the dataframe so as to convert it into numeric 
for col in pew_earn:
    pew_earn[col] = pew_earn[col].str.replace('$', '')
    pew_earn[col] = pew_earn[col].str.replace(',', '')
    pew_earn[col][pew_earn[col] == 'no data'] = None
    
pew_earn.drop(pew_earn.tail(1).index,inplace=True)

numeric_col2 = list(pew_earn.columns)
numeric_col2 = numeric_col2[-1:] + numeric_col2[:-1]
pew_earn = pew_earn[numeric_col2]
numeric_col2 = numeric_col2[2:] 
for col in numeric_col2:
    pew_earn[col] = pew_earn[col].astype(float)

# convert from wide to long format
pew_earn_clean = pd.melt(pew_earn, id_vars = ['state', 'MSA', 'FIPS'], 
        value_vars=['16+_2019_dollars_women',
       '16+_2019_dollars_men', '16+_2000_dollars_women',
       '16+_2000_dollars_men', '16_29_2019_dollars_women',
       '16_29_2019_dollars_men', '16_29_2000_dollars_women',
       '16_29_2000_dollars_men', '30_49_2019_dollars_women',
       '30_49_2019_dollars_men', '30_49_2000_dollars_women',
       '30_49_2000_dollars_men', '50+_2019_dollars_women',
       '50+_2019_dollars_men', '50+_2000_dollars_women',
       '50+_2000_dollars_men'])
pew_earn_clean.rename(columns={'value':'income'}, inplace=True)

# cleaning up the dataframe to represent one individual entry as a spcific age-year-gender-MSA combination
pew_earn_clean['age'], pew_earn_clean['yearval'] = pew_earn_clean['variable'].str.split('_', 1).str
pew_earn_clean = pew_earn_clean.drop('variable', axis=1)
pew_earn_clean['age'] = pew_earn_clean['age'].apply(lambda x: '16-29' if  x == '16' else x)
pew_earn_clean['age'] = pew_earn_clean['age'].apply(lambda x: '30-49' if  x == '30' else x)
pew_earn_clean['age'] = pew_earn_clean.age.astype('category')

pew_earn_clean['gender'] = pew_earn_clean['yearval'].str.extract('(20.*)')[0]
pew_earn_clean = pew_earn_clean.drop('yearval', axis=1)
pew_earn_clean['year'] = pew_earn_clean['gender'].str[:4]
pew_earn_clean["year"] = pd.to_numeric(pew_earn_clean["year"])

pew_earn_clean['gender'] = pew_earn_clean['gender'].str[13:]
pew_earn_clean['gender'] = pew_earn_clean.gender.astype('category')

pew_earn_clean = pew_earn_clean[['FIPS', 'MSA', 'state', 'age', 'year', 'gender', 'income']]

# convert dataframe into geopandas so as to plot median annual earnings for men and women 
pew_earn_final = pew_earn_clean.merge(msa, left_on='FIPS', right_on='GEOID', how = 'inner')
pew_earn_final = pew_earn_final.drop('GEOID', axis=1)

pew_earn_final = gpd.GeoDataFrame(pew_earn_final)    

# =========================================================================================================
# Saving the cleaned data sets onto the dekstop, and they were manually added to drive (linked in READme)
# =========================================================================================================

#pew_earn_final.to_csv(r'/Users/arunimamehrotra/Desktop/median annual earnings.csv')
#pew_perc_final.to_csv(r'/Users/arunimamehrotra/Desktop/womens wages as percentage of mens.csv')

# =========================================================================================================
#                                   SHINY INTERACTIVE PLOTS
# =========================================================================================================

img_url = "https://cdn-icons-png.flaticon.com/512/6756/6756032.png"

app_ui = ui.page_fluid(
    ui.row(
        ui.column(4, ui.img(src=img_url, height=90, width=134)),
        ui.column(8, ui.h2('The Gender Wage Gap in America', align = 'left'), ui.hr())),
    ui.row(
        ui.column(9, 
                  ui.row(ui.input_select(id = 'selectyear',
                                     label = 'Choose Year',
                                     choices = [2000, 2019])),
                  ui.row(ui.input_select(id = 'selectage1',
                                               label = 'Choose Age Bracket for Choropleth',
                                               choices = ['16+', '16-29', '30-49', '50+']))),
        ui.column(3, 
                  ui.row(ui.input_select(id = 'selectgender',
                                     label = 'Choose Gender',
                                     choices = ['women', 'men'])),
                  ui.row(ui.input_select(id = 'selectage2',
                                     label = 'Choose Age Bracket',
                                     choices = ['16+', '16-29', '30-49', '50+']))), align = 'center'),
    ui.row(
        # interactive plots 
        ui.column(8, ui.output_plot('womenwageperc')),
        ui.column(4, ui.output_plot('medianannualearnings'))
        ),
    ui.row(
        ui.h2("Reddit Gender Sentiments", align = 'center')
        ),
    ui.row(
        # text processing 
        ui.column(6, ui.output_image('sentiment_dist_image'),align = 'center'),
        ui.column(6, ui.output_image('title_polarity_vs_post_score_image'),align = 'center')
        ),
    ui.row(
        ui.h2("Occupation Feminization", align = 'center')
        ),
    ui.row(
        # regression analysis 
        ui.column(8, ui.output_image('occ_fem_wage_image'),align = 'center'),
        ui.column(4, ui.output_image('occ_gend_dist_image'),align = 'center')
        ),
    ui.row(
        ui.h3("OLS Regression", align = 'center')
        ),
    ui.row(
        ui.output_image('OLS_results_image'), align = 'center')
    )


def server(input, output, session):
    
    @output
    @render.plot
    def womenwageperc():
        
        fig, ax = plt.subplots(figsize=(15,15), dpi = 100)

        
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.1)
        
 
        x = input.selectyear() 
        x = np.int64(x)
        data = pew_perc_final.loc[pew_perc_final['year'] == x] 
        
        data = data.loc[data['age']== input.selectage1()]                       
    
        
        ax = data.plot(ax=ax, column=data['percentage'], legend=True, cax=cax, 
                       edgecolor='black',  linewidth=0.5, cmap = "Paired", alpha = 0.8)
        ax.axis('off')
        ax.set_title('Women’s wages as a Percentage of Men’s wages across MSAs in America')
        
    @output
    @render.plot
    def medianannualearnings():
        
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(plt.MaxNLocator(1))
        
        data2 = pew_earn_final.loc[pew_earn_final['age'] == input.selectage2()]
        data2 = data2.loc[data2['gender']== input.selectgender()]  
        
        ax.bar(data2['year'], data2['income'], width=3, color = 'darkorange')
        ax.set_xlabel('Year')
        ax.set_ylabel('Median income in US $')
        ax.set_ylim([0, 120000])
        ax.set_title('Median annual earnings \n of ' + input.selectgender() + 
                     ' belonging to age group:' + input.selectage2())
        
    @output
    @render.image
    def sentiment_dist_image():
        
        from pathlib import Path

        dir = Path(r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/').resolve()
        img: ImgData = {"src": str(dir/'Sentiment_dist.png'), "width": "300px"}
        return img

    @output
    @render.image
    def title_polarity_vs_post_score_image():
        
        from pathlib import Path
    
        dir = Path(r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/').resolve()
        img: ImgData = {"src": str(dir/'Title Polarity_vs_Post Score.png'), "width": "400px"}
        return img

    @output
    @render.image
    def occ_gend_dist_image():
        
        from pathlib import Path
    
        dir = Path(r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/').resolve()
        img: ImgData = {"src": str(dir/'occ_gend_dist.png'), "width": "400px"}
        return img

    @output
    @render.image
    def occ_fem_wage_image():
        
        from pathlib import Path
    
        dir = Path(r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/').resolve()
        img: ImgData = {"src": str(dir/'occ_fem_wage.png'), "width": "700px"}
        return img
    
    @output
    @render.image
    def OLS_results_image():
        
        from pathlib import Path
    
        dir = Path(r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/').resolve()
        img: ImgData = {"src": str(dir/'OLS_results.png'), "width": "400px"}
        return img



app = App(app_ui, server)

# =========================================================================================================

# SOURCES: 
    # https://www.easytweaks.com/drop-columns-name-pandas-dataframes/
    # https://stackoverflow.com/questions/38516481/trying-to-remove-commas-and-dollars-signs-with-pandas-in-python
    # https://stackoverflow.com/questions/26921651/how-to-delete-the-last-row-of-data-of-a-pandas-dataframe
    # https://stackoverflow.com/questions/14745022/how-to-split-a-dataframe-string-column-into-two-columns
    # https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/
    # https://stackoverflow.com/questions/18434208/pandas-converting-to-numeric-creating-nans-when-necessary
    # https://stackoverflow.com/questions/18434208/pandas-converting-to-numeric-creating-nans-when-necessary
    # https://towardsdatascience.com/reshaping-a-pandas-dataframe-long-to-wide-and-vice-versa-517c7f0995ad
    # https://datatofish.com/if-condition-in-pandas-dataframe/
    # https://stackoverflow.com/questions/60063716/pandas-dataframe-extract-string-between-two-strings-and-include-the-first-deli
    # https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
    # https://stackoverflow.com/questions/39092067/pandas-dataframe-convert-column-type-to-string-or-categorical
    # https://docs.bokeh.org/en/test/docs/user_guide/plotting.html
    # https://stackoverflow.com/questions/6682784/reducing-number-of-plot-ticks
    # https://shiny.rstudio.com/py/api/reference/shiny.ui.output_image.html
    
# =========================================================================================================
    


