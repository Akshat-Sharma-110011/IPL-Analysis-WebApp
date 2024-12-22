# IPL-Analysis-WebApp

IPL Analysis Project

Overview

The IPL Analysis Project is an interactive web application designed for comprehensive analysis of IPL cricket match datasets. It uses Streamlit for the user interface, allowing users to explore data and visualize trends effortlessly. The application provides insights through various analysis types, including overview, year-wise, and team-wise breakdowns.

Features

Overview Analysis: Displays dataset statistics, toss decisions, match results, and more.

Year Wise Analysis: Allows users to analyze data for specific years and parameters such as winners, runs, and super overs.

Team Wise Analysis: Insights into team performances, match outcomes, and detailed pair-wise match statistics.

Data Visualizations: Interactive charts and graphs powered by Plotly and Matplotlib.

Prerequisites

Python 3.8 or higher

Libraries:

Streamlit

Pandas

Plotly

Matplotlib

Seaborn

Installation

Clone the repository:

git clone <repository_url>

Navigate to the project directory:

cd ipl-analysis

Install the required dependencies:

pip install -r requirements.txt

Usage

Run the Streamlit application:

streamlit run app.py

Open the displayed URL in your web browser.

File Structure

app.py: Main application script.

matches.csv: Dataset containing IPL match details.

PngItem_1270088.png: IPL logo image used in the sidebar.

Functionality Breakdown

Overview Analysis

Displays dataset overview: rows, columns, and sample data.

Provides key statistics like total seasons, match types, toss decisions, and results.

Offers a downloadable version of the dataset.

Year Wise Analysis

Filters data by selected years and analysis types.

Visualizes trends such as player of the match, winners, runs distribution, and win margins.

Team Wise Analysis

Highlights matches played and won by each team across seasons.

Generates heatmaps and pairwise team statistics.

Allows detailed filtering by teams, seasons, match types, and venues.

Data Visualizations

Bar Charts: For player of the match and toss decision analysis.

Pie Charts: For winner and super-over distributions.

Histograms: For result margins, target runs, and overs.

Heatmaps: For team match participation.

Dataset

Path: D:\DA Projects\IPL\matches.csv

Contains columns such as season, team1, team2, winner, result_margin, target_runs, super_over, etc.

Screenshots

Include relevant screenshots of the application interface and visualizations.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

License

This project is licensed under the MIT License.
