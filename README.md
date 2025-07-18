
## PPHA30538: Final Project 

### Repository name: final-project-dpii_final_uz_sb_am
_final-project-dpii_final_uz_sb_am created by GitHub Classroom_

# The Wage Gap in America: Occupation Feminisation and its effect on median wages

# Group members: Saloni Bhardwaj, Arunima Mehrotra, Umama Zillur

## Notes

The source data for RegressionAnalysis.py is too large and was manually uploaded on drive at this link: [IPUMS raw data](https://drive.google.com/file/d/1Oe1soB6mxvGII7VoxGWyfW3q8CZt6V9d/view?usp=sharing)

Order of Operation: Start with the Data Analysis, then with the text and sentiment analysis, and then with interactive plotting and shiny! 
1. [womens wages as percentage of mens](https://drive.google.com/file/d/1uhx6UA_G7LWs3faXIy4gCD6vzQjBvMxY/view?usp=sharing)
2. [median annual earnings](https://drive.google.com/file/d/1Pa4omwSBd_3GJ-31H67MZINAv01XMiaG/view?usp=sharing)
Paths have been set according to our personal folders:
1. For shinyplotting.py, base_path = r'/Users/arunimamehrotra/Documents/GitHub/final-project-dpii_final_uz_sb_am/Data', which is where the raw data is stored for one coding member. This will have to be changed accordingly. 
2. For RegressionAnalysis.py, path = r'/Users/umamazillur/Documents/GitHub/final-project-dpii_final_uz_sb_am/Data', which is where raw data is stored for the other coding member. This will have to be changed accordingly. 

## Description

This project focuses on exploring the gender pay gap in several US industries and occupations from US Census data. Even about half a century after the ‘Equal Pay Act’ was passed to abolish sex based discrimination in wages, women still earn less than men.
We aim to analyze one of the causes of the gender wage gap - gendered devaluation of occupations and work associated with women. Specifically, we will analyze whether an occupation’s sex composition affects its median wages. By using census panel data, we studied the effect of an occupation’s proportion of females on the log of median wages for males and females.

Another component of the project performs text analysis on online communities to determine the nature of discourse around women. The intention of this exploration is to understand the narrative around women's rights and lived realities in the digital age. Language shapes attitudes and online forums are quickly becoming a catalyst for extremist behaviour both online and offline. Python text analysis presents a robust tool to conduct this exploration. 

## Project Components: 

1. Data Analysis: Regression analysis of panel data @umama 
2. Interactive plots: Using a shiny app, we visualise and compare the pay gap across US Metropolitan Statistical areas between 2000 and 2019. 
3. Text and sentiment analysis: We scrape two popular subreddits : MensRights and antifeminists to get a sense of what is the popular rhetoric in public forums. _*TRIGGER WARNING*: The scraped data contains explicit language, often accompanied with mention of violence, abuse and assault. Readers are advised to proceed with discretion._  
  The libraries used are spacy and nltk to do a preliminary sentiment and polarity analysis.

### Top-level directory layout

    .
    ├── RegressionAnalysis.py                 # Data cleaning, analysis and model fitting from IPUMS data
    ├── ShinyPlotting.py                      # Interactive plotting from Pew center data
    ├── RedditTextAnalysis.py                 # Text analysis from subreddit data
    ├── Images                                # Generated static plots
    ├── Data                                  # Original raw datasets and processed data files 
    └── README.md


### Datasets and API: 
1. IPUMS USA : Individual level US Census data on the following key variables 
  i. EDUC: Educational attainment
  ii. OCC1950: Occupation classification
  iii. IND1950: Industry classification 
  iv. WKSWORK2: Weeks worked last year
  v. HRSWORK2: Hours worked last week 
  vi. INCWAGE: Wage and salary income
  vii. CPI99:	CPI-U adjustment factor to 1999 dollars
  viii. REGION: Census region and division
  ix. SEX: Gender of individual
SOURCE: IPUMS USA: https://usa.ipums.org/usa/index.shtml

While the whole data cleaning and manipulation is in 'RegressionAnalysis.py' and the final dataset 'ipums_final.csv' is in this repository, the source data is too large and was manually uploaded on drive at this link: https://drive.google.com/file/d/1Oe1soB6mxvGII7VoxGWyfW3q8CZt6V9d/view?usp=sharing

2. Pew Center Dataset for MSA-level earnings data
3. U.S., Current Metropolitan Statistical Area/Micropolitan Statistical Area (CBSA) National: : [here](https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-metropolitan-statistical-area-micropolitan-statist)
4. PRAW: The Python Reddit API Wrapper: [Documentation](https://praw.readthedocs.io/en/stable/#praw-the-python-reddit-api-wrapper)

The final datasets from Pew Research are uploaded on drive, and while they are not called on python since we created them within the code, they are used for the interactive plotting and analysis. While the whole data cleaning and manipulation is in 'shinyplotting.py', the saving has been commented out and the files were manually uploaded on drive. They are as follows: 
1. [womens wages as percentage of mens](https://drive.google.com/file/d/1uhx6UA_G7LWs3faXIy4gCD6vzQjBvMxY/view?usp=sharing)
2. [median annual earnings](https://drive.google.com/file/d/1Pa4omwSBd_3GJ-31H67MZINAv01XMiaG/view?usp=sharing)

## Writeup

### Research question

Through this research we aim to analyze one of the causes of the gender wage gap - gendered devaluation of occupations and work associated with women. Specifically, we analyze whether an occupation’s sex composition affects its median wages. By using panel data from 1950 to 1990, we will study the effect of an occupation’s proportion of females on the log of median wages for males and females. We further explore the issue of the gender wage gap by seeing how gender wage gap has changed from 2000 to 2019 in certain MSAs. The analysis is subsetted by multiple age groups because the positionality of women is deeply intertwined with their child-bearing abilities, and thereby, age is an essential to know where a woman stands under a patriarchal society's gaze. 

Since the issue of the gender wage gap is an issue of rights - deeply tangled with gender norms and our socio-cultural, we chose to supplement the wage analysis with an examination of the discourse surrounding the broad theme of women's rights using content on Reddit.

### Coding involved 

#### Text analysis: 
The data was collected using the Python Redddit API Wrapper (PRAW). The app is setup on a local script for personal use within the the http://localhost:8080 uri. The client id, secret and user id are all included in the code. PRAW presents an efficient approach to access reddit post submission attributes such as title, body, score, likes, comments, etc. 

Two popular subreddits were selected to scrape the top posts: MensRights and antifeminsists. The scraped data is stored in a dataframe which is written to a csv for easy access without API as well. 
Using spacy functionality We calculate polarity scores on the title and body of the posts. For the plot, the polarity of just the titles is plotted against the post 'score' attribute. 
As an addendum , we also explored the same praw object with nltk to calculate polarity and adding labels to the posts. The resultant plot shows distribution of posts across positive, neutral and negative labels. 

#### Shiny and Interactive Plotting: 

For the interactive plots we utilized data from Pew Research Center. They have released data on the Wage Gap by Meteropolitian Area for the years 2000 and 2019. This dataset includes annual median earnings of women and men, as well as women's wages as percentages of men's wages for the both years. The dataset is further divided into age groups (16 - 29, 30 - 49, 50+) as well as a grouping encapsultaing the whole working demogrpahic (16+). Through data cleaning and manipulation, we converted the dataset from wide to long format, and in the end had two datasets - one for percentage wages, and other for annual median earnings. 

For the first plot, we created an interactive chloropleth which maps Women's wages as percentage of Men's wages for all MSAs the dataset has, based on the age group and the year. The second plot is also an interactive plot which displays the Median Annual Earnings based on the selected gender and age bracket. 

#### Regression Analysis 

IPUMS USA Census data was downloaded for the years 1950 through 2019 with ten year intervals. Since, the same variable on hours worked was not available for all yeara in our sample, the latest year in our sample is 1990. All household level variables were excluded from the analysis. Wage variables were created using annual income data from IPUMS. Data regarding the number of weeks worked and number of hours worked per week for were taken from IPUMS to construct the hourly wage. Since the IPUMS database provides intervalled data for weeks worked per year and hours worked last week, the average of each range was taken. For hours worked, IPUMS provided categorical data which were then transformed to a continuous variable. The calculated hourly wage was then adjusted for inflation using the cpi99 variable from IPUMS. Wage data was logged for final analysis. The industry variable was created by consolidating the industries provided by IPUMS into 9 broad industries. For the unit of analysis, the occupation variable was cross classified with the industry variable to create industry-occupation pairs. This was required as wages for the same occupation vary widely depending on the industry that they are part of. For the purpose of our paper, occupation will refer to each occupation industry cell. While all industries were included, given the granularity of the occupation data, only the most common occupations were chosen. Education data excluded those below highschool graduates. The REGION variable was transformed into four main regions. The individual level census data was grouped by occupation, industry and year and then used to calculate ratio of individuals at different education levels and different regions within each occupation for each of the five years in our sample. The individual level sex data was used to calculate the ratio of females to males in each occupation within each year. An occupation is considered to be ‘female’ if the proportion of female in the occupation industry cell is between 67-100%, ‘male’ if 0-33% and ‘mixed’ otherwise. 

For the regression analysis, the dependent variable of the median log wage and the independent variables were levels of education, four regions, and ratio of females to males. We used a simple OLS model as well as a fixed effects model to account wage variation over time. 

### Weaknesses or difficulties encountered

#### Text analysis: 

Since alot of the Reddit posts are wide-ranging in subject matter, we can't extract the appropriate polarity analysis due to how language and discourse in these spaces occur. Furthermore, many posts also have memes and videos which are essential currency in the interct space to convey sentiments; because we did not scrape the images and videos, we do not have access to the polarity scores in that regard. Lastly, we recognize that we can't conclude much from a polarity based sentiment analysis because gender sentiments are multidimensional and require a more nuanched research. 
In addition, making repeated requests through the API created problem because after a point it stopped responding and gave HDPT 404 errors. 

#### Shiny and Interactive Plotting: 

For the Pew Research Center's data, the biggest weakness was the scarcity of data. Only few MSAs were captured by the data and it covered only the years 2000 to 2019. Therefore, this analysis of Wage Gap is only the tip of the iceberg since we can't see the trend in detail. 

#### Regression Analysis 

Given the size of the IPUMS data, it was not possible to work with it which is why we had to resort to using a subset of our full sample for our analysis. We used the IPUMS USA website which has an option to create subsets of the full sample. However, this affected the original weights for each of the years included in our sample. Not being able to include more recent years in our analysis was a major weakness as much of the major shifts in occupation feminization has taken place in the last decade. 


### Brief discussion of results

#### Text analysis: 

The first static plot under the heading 'Reddit Gender Sentiments' shows us that the majority of posts when we scrape reddit regarding the topic Men's rights and anti-feminists is neutral in nature, followes by negative, and then positive sentiments. However, the drop from negative to positive is quite stark (12% approximately) which goes to show that discourse surrounding these topics is associated with negative language/emotions/sentiments. 

In addition to the distribution of posts on this topic, we also analyzed which category of posts gains attraction. In the second static plot, we can observe that the range of negative posts is much larger, and that while neutral posts get the most likes, slightly negtaive posts also obtian very high interaction. 

#### Shiny and Interactive Plotting: 

The first interactive plot which is also a chloropleth shows us that majority of Women's wages as percentage of Men's wages in 2000 is around the 70 to 80% category for all ages above 16. For 2019, this wage percentage has slowly shifted to the 80 to 85% majority. It is interesting to note that the areas with higher percentages in 2000 are still at the higher end of the spectrum in 2019. As for breakdown due to age group categories, in 2000 women ages 16-29 held majority 80 to 90% of men's wages, for those aged 30-49 the majority earned 70 to 80% of men's wages, and for those ages 50+ the majority earned 60 to 70%. However, for the year 2019, women ages 16-29 held majority 85 to 95% of men's wages, for those aged 30-49 the majority earned 75 to 85% of men's wages, and for those ages 50+ the majority earned 70 to 80%. Therefore, in both years it has been the trend that as women age, they earn less and less as a percentage of male earnings. 

This is also shown in the second interactive plot which tracks annual median earnings based on gender and age bracket for 2000 and 2019. Overall, in all ages above 16+, men in 2000 and 2019 have earned somewhere between 85K to 90K while women have earned between 60K to 62K. However, what is devastating is how women between ages 16-29 earned around 50K in both years, 70K as they enterd the 30-49 age bracket, and remained the same in 50+ age bracket. Comapre this to men who earned around 55K when they were 16-29, and a shocking spike up to 90K to 110K once they are in the 30-49 age bracket, and a stabilization to 100K once they reach 50+. The jump in the age group 30-49 between men and women is humongous (around 25K annually), and this trend has persisted from 2000 to 2019. This is the age when many women start becoming mothers as well;  the skewed earnings ratio not only are a reflection of how society regards women, or rather motherhood, but also impacts children's life trajectory in tangible ways. 

#### Regression Analysis 

Figure: Occupation Gender Distribution 
This figure presents a comparison of the distribution of occupation genders across all the years in our study. We see that 'male' occupations consistently make up the majority of the market. There is also a steady increase in the 'mixed' category of occupations over the years reflecting more women entering the job market. The share of 'female' occupations does not shift significantly and hovers around 30% of the market throughout the years. 

Figure: Impact of Occupation Feminization on Wages

This figure compares wage trend for females and males across the three occupation categories - 'male, 'female' and 'mixed. Unsurprisingly, we see that males earn higher across all three categories. In addition, we see that for both genders, it is most favorable to be working in 'male' occupations which have higher wage compared to 'mixed' and 'female' occupations. For females, the difference in wage between 'mixed' and 'female' categories is much higher than for males. 

Figure: OLS Results
Plotting results of our simple OLS regression produces a downward sloping regression line showing the negative relationship between ratio of females within an occupation and the median log wage of that occupation. We can see that the model predicts as ratio of female increases, median log wage will decrease. 

Fixed Effects: 

OLS Regression Results                            
==============================================================================
Dep. Variable:        LOG_MEDIAN_WAGE   R-squared:                       0.428
Model:                            OLS   Adj. R-squared:                  0.427
Method:                 Least Squares   F-statistic:                     411.1
Date:                Wed, 07 Dec 2022   Prob (F-statistic):          5.46e-134
Time:                        21:10:37   Log-Likelihood:                -171.68
No. Observations:                1101   AIC:                             349.4
Df Residuals:                    1098   BIC:                             364.4
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==============================================================================
coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const        -20.3490      1.699    -11.979      0.000     -23.682     -17.016
FEM_RATIO     -0.7251      0.028    -25.744      0.000      -0.780      -0.670
YEAR           0.0118      0.001     13.719      0.000       0.010       0.014
==============================================================================
Omnibus:                       60.933   Durbin-Watson:                   0.770
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               78.214
Skew:                          -0.516   Prob(JB):                     1.04e-17
Kurtosis:                       3.800   Cond. No.                     3.92e+05
==============================================================================                                           

PooledOLS Estimation Summary                          
================================================================================
Dep. Variable:        LOG_MEDIAN_WAGE   R-squared:                        0.4800
Estimator:                  PooledOLS   R-squared (Between):              0.9948
No. Observations:                  12   R-squared (Within):              -0.0690
Date:                Wed, Dec 07 2022   R-squared (Overall):              0.4800
Time:                        21:11:02   Log-likelihood                    1.5970
Cov. Estimator:            Unadjusted                                           

F-statistic:                      9.2302

Entities:                           3   P-value                           0.0125
Avg Obs:                       4.0000   Distribution:                    F(1,10)
Min Obs:                       4.0000                                           
Max Obs:                       4.0000   F-statistic (robust):             9.2302
P-value                           0.0125
Time periods:                       4   Distribution:                    F(1,10)
Avg Obs:                       3.0000                                           
Min Obs:                       3.0000                                           
Max Obs:                       3.0000                                           

Parameter Estimates                              
==============================================================================
Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
------------------------------------------------------------------------------
const          2.8554     0.1125     25.388     0.0000      2.6048      3.1060
FEM_RATIO     -0.6401     0.2107    -3.0381     0.0125     -1.1095     -0.1706
==============================================================================

The Fixed Effects model shows that if the ratio of females in an occupation increases by one unit, log median wage will decrease by 47%. The p value is less than alpha (0.05) and so it is statistically signifcant. The high R squared value of 0.48 tells us that 48% of the variability observed in our wage variable is explained by the regression model. While the simple OLS as well as the Pooled OLS model both show statistically signifcant coefficients, there are some differences. The simple OLS model shows that ratio of female decreases median wage even more. 


### How this could be fleshed out in future research 
Incorporating recent data on occupations can help strengthen this research. Firstly, our occupation and industry data from IPUMS relies on classifications from the 1950s. There has been drastic changes in the nature of work associated with each occupation and industry and our study is unable to take that into account. Many contemporary occupations and industries had to be collapsed based on the outdated classifications.

Even though our fixed effects model captured time invariant occupation characteristics, it was still unable to account for occupations/industry characteristics that changed over time. We can assume there has been drastic changes in skills demands, training requirements, work hours etc. Further understanding of the gender wage gap requires exploration of other factors such as causes of occupational segregation, industry barriers, employer discrimination, gender based job preferences etc. 
