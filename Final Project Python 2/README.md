# The Wage Gap in America: Occupation Feminization and Its Effect on Median Wages

This project investigates the persistent gender wage gap in the U.S., with a specific focus on whether an occupation’s gender composition influences its median wages. The work was completed as the final project for the graduate-level course **PPHA 30538: Data and Programming for Public Policy II** at the University of Chicago.

## Repository Contents

| File/Folder              | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `RegressionAnalysis.py`  | Wage regression analysis using IPUMS Census data                            |
| `ShinyPlotting.py`       | Interactive Shiny app using Pew MSA earnings data                          |
| `RedditTextAnalysis.py`  | Sentiment analysis of Reddit discourse on gender                            |
| `Images/`                | Static plots and visualizations                                             |
| `Data/`                  | Processed datasets from IPUMS, Pew, and Reddit                              |
| `README.md`              | This file : overview, documentation, and summary of the project             |


## Project Overview

Despite the passage of the Equal Pay Act over 50 years ago, the gender pay gap remains. Our work explores one key driver: **the devaluation of occupations as they become female-dominated**. We use census microdata to examine the relationship between the proportion of females in an occupation and that occupation’s median wage.

The project also includes:
- **Reddit-based sentiment analysis** of discussions on gender rights
- **Interactive data visualizations** showing wage trends by metro area and age bracket

---

## Key Questions

- Does an occupation’s feminization correlate with lower wages?
- How does the wage gap vary by age and geography across U.S. metro areas?
- What does online discourse say about gender and work?

---

## Project Components

### Regression Analysis (1950–1990, IPUMS Data)
- Constructed **hourly wages** using income, hours, and weeks worked
- Grouped by **occupation-industry-year** to define unit of analysis
- Created categorical variable for occupation gender composition (male, female, mixed)
- Applied **OLS and Fixed Effects models** to study the relationship between gender ratio and log median wages

###  Interactive Visualizations (2000–2019, Pew Data)
- Used Pew MSA-level data on **median earnings by gender and age group**
- Created **Shiny app** with:
  - A choropleth mapping women's earnings as % of men’s across metros
  - Interactive comparison of **median earnings** by gender, age, and year

### 3. Reddit Text & Sentiment Analysis
- Scraped posts from **r/MensRights** and **r/antifeminists** using `PRAW`
- Used **SpaCy** and **NLTK** to calculate sentiment polarity
- Plotted sentiment scores vs. post engagement (likes, comments)


---

##  Summary of Findings

- **Occupation Feminization** is negatively correlated with median wages (statistically significant).
- **Interactive maps** show modest improvements in wage parity from 2000 to 2019—but a persistent gap remains, especially in older age groups.
- **Reddit analysis** reveals largely neutral to negative sentiment around gender-related topics, with high engagement on negative posts.

---

## Sample Regression Result (OLS)

| Variable        | Coefficient | p-value  |
|----------------|-------------|----------|
| Female Ratio   | -0.7251     | < 0.001  |
| Year           | +0.0118     | < 0.001  |

> A 1-unit increase in female ratio is associated with a **47% decrease in log median wage**, controlling for year and other variables.

---

##  Tools & Libraries

- `pandas`, `numpy`, `matplotlib`, `seaborn`
- `geopandas`, `shapely` for mapping
- `spacy`, `nltk`, `PRAW` for NLP and Reddit scraping
- `Shiny for Python` for interactive plotting

---

## Future Directions

- Update with newer occupation classifications post-2000
- Model other variables: occupational segregation, job access barriers, employer bias
- Expand text analysis with multimodal data (e.g., image memes, video content)
- Add interactive filtering by race, education, or region

---

## Team

- **Saloni Bhardwaj**  
- **Arunima Mehrotra**  
- **Umama Zillur**

---

##  Data Sources

- **[IPUMS USA](https://usa.ipums.org/usa/)** – U.S. Census microdata  
- **[Pew Research Center](https://www.pewresearch.org/)** – Gender wage data by MSA  
- **[Reddit API (PRAW)](https://praw.readthedocs.io/)** – Public discourse scraping  

---

🔍 *This repository is shared for educational and professional showcase purposes. Raw data files have not been added due to size constraints.*
