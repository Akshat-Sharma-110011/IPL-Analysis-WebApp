import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"D:\DA Projects\IPL\matches.csv"
df = pd.read_csv(file_path)

st.markdown(
    "<h1 style='text-align: center; color: black;'>IPL Analysis</h1>",
    unsafe_allow_html=True
)
st.markdown('---')
st.sidebar.image(r"D:\DA Projects\IPL\PngItem_1270088.png")

# Sidebar for navigation
option = st.sidebar.selectbox(
    "Choose an option",
    ["Overview Analysis", "Year Wise Analysis", "Team Wise Analysis"]
)

# Overview Analysis Page
if option == "Overview Analysis":
    st.markdown("<h3>Overview of the Dataset</h3>", unsafe_allow_html=True)

    # Display basic information with larger font sizes
    st.markdown("<h3>Dataset Overview:</h3>", unsafe_allow_html=True)
    st.write(f"**Number of Rows**: {df.shape[0]}")
    st.write(f"**Number of Columns**: {df.shape[1]}")
    st.markdown("---")

    # Show the first few rows of the dataset below the overview
    st.markdown("<h3>First 5 Rows of the Dataset:</h3>", unsafe_allow_html=True)
    st.table(df.head())
    st.markdown("---")

    # Total number of seasons and count
    total_seasons = df['season'].nunique()
    st.markdown(f"<h3>Total Number of Seasons: {total_seasons}</h3>", unsafe_allow_html=True)

    # Display seasons in a grid (dummy columns for layout)
    seasons = sorted(df['season'].unique())
    columns = st.columns(4)  # Divide into 4 columns for better grid layout
    for i, season in enumerate(seasons):
        columns[i % 4].markdown(f"- {season}")
    st.markdown("---")

    # Total number of different match types
    total_match_types = df['match_type'].nunique()
    st.markdown(f"<h3>Total Number of Match Types: {total_match_types}</h3>", unsafe_allow_html=True)

    # Display match types in a grid (dummy columns for layout)
    match_types = df['match_type'].unique()
    columns = st.columns(4)  # Divide into 4 columns
    for i, match_type in enumerate(match_types):
        columns[i % 4].markdown(f"- {match_type}")
    st.markdown("---")

    # Most common toss decision
    most_toss_decision = df['toss_decision'].value_counts().idxmax()
    toss_decision_count = df['toss_decision'].value_counts().max()
    st.markdown("<h3>Most Common Toss Decision:</h3>", unsafe_allow_html=True)
    st.markdown(f"- {most_toss_decision} ({toss_decision_count} times)")
    st.markdown("---")

    # Most common match result (runs or wickets)
    most_common_result = df['result'].value_counts().idxmax()
    result_count = df['result'].value_counts().max()
    st.markdown("<h3>Most Common Result Type:</h3>", unsafe_allow_html=True)
    st.markdown(f"- {most_common_result} ({result_count} times)")
    st.markdown("---")

    # Highest result margin
    highest_margin = df['result_margin'].max()
    st.markdown("<h3>Highest Result Margin:</h3>", unsafe_allow_html=True)
    st.markdown(f"- {highest_margin}")
    st.markdown("---")

    # Highest target runs
    highest_target_runs = df['target_runs'].max()
    st.markdown("<h3>Highest Target Runs:</h3>", unsafe_allow_html=True)
    st.markdown(f"- {highest_target_runs}")
    st.markdown("---")

    # Total number of super overs
    total_super_overs = df['super_over'].value_counts().get('Y', 0)
    st.markdown("<h3>Total Number of Super Overs:</h3>", unsafe_allow_html=True)
    st.markdown(f"- {total_super_overs}")
    st.markdown("---")

    # Add a download button for the dataset
    st.markdown("<h3>Download the Dataset:</h3>", unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Dataset as CSV",
        data=csv,
        file_name="cricket_match_data.csv",
        mime="text/csv",
    )

# Year Wise Analysis Page
elif option == "Year Wise Analysis":
    st.markdown("<h3>Year Wise Analysis</h3>", unsafe_allow_html=True)

    # Sidebar widgets for year and analysis type selection
    st.sidebar.header("Year Wise Analysis Settings")
    selected_option = st.sidebar.selectbox(
        "Choose Analysis Type",
        ["Player of the Match", "Winner", "Runs", "Win Range", "Super Over"]
    )

    selected_years = st.sidebar.multiselect(
        "Choose Years",
        options=sorted(df['season'].unique()),
        default=sorted(df['season'].unique())  # Default to all years selected
    )

    # Filter data by selected years
    df_filtered = df[df['season'].isin(selected_years)]

    # Display the selected options and years with larger font size
    st.markdown(f"<h3>Selected Years: {', '.join(map(str, selected_years))}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3>Selected Analysis Type: {selected_option}</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Analysis based on selected options
    if selected_option == "Player of the Match":
        st.markdown("<h4>Player of the Match Analysis</h4>", unsafe_allow_html=True)
        player_of_the_match = df_filtered['player_of_match'].value_counts().reset_index()
        player_of_the_match.columns = ['Player', 'Count']

        # Plotting Player of the Match Distribution
        fig = px.bar(player_of_the_match, x='Player', y='Count', title='Player of the Match Distribution')
        st.plotly_chart(fig)

    if selected_option == "Winner":
        st.markdown("<h4>Winner Analysis</h4>", unsafe_allow_html=True)
        winner_count = df_filtered['winner'].value_counts().reset_index()
        winner_count.columns = ['Winner', 'Count']

        # Plotting Winner Count
        fig = px.pie(winner_count, names='Winner', values='Count', title='Wins per Team')
        st.plotly_chart(fig)

    if selected_option == "Runs":
        st.markdown("<h4>Runs Analysis</h4>", unsafe_allow_html=True)

        # Melting data for univariate analysis
        runs = df_filtered[['season', 'team1', 'team2', 'target_runs']].melt(
            id_vars=['season', 'team1', 'team2'], value_vars=['target_runs'], var_name='Run Type', value_name='Runs'
        )

        # Plotting Runs as a univariate analysis (histogram)
        plt.figure(figsize=(10, 6))
        sns.histplot(runs['Runs'], kde=True, bins=30)
        plt.title('Distribution of Runs')
        plt.xlabel('Runs')
        st.pyplot()
        st.markdown("---")

    if selected_option == "Win Range":
        st.markdown("<h4>Win Range Analysis</h4>", unsafe_allow_html=True)
        # Analyzing the result margin (win range)
        win_range = df_filtered['result_margin'].dropna()

        # Plotting the win range as a histogram
        plt.figure(figsize=(10, 6))
        sns.histplot(win_range, kde=True, color='green', bins=30)
        plt.title('Distribution of Win Margin')
        plt.xlabel('Win Margin')
        st.pyplot()

    if selected_option == "Super Over":
        st.markdown("<h4>Super Over Analysis</h4>", unsafe_allow_html=True)
        super_over_count = df_filtered['super_over'].value_counts().get('Y', 0)

        # Display the count of super overs
        st.write(f"Total Super Overs: {super_over_count}")
        # Plotting Super Overs
        fig = px.pie(names=['No Super Over', 'Super Over'],
                     values=[len(df_filtered) - super_over_count, super_over_count],
                     title='Super Over Distribution')
        st.plotly_chart(fig)

# Team Wise Analysis Page
elif option == "Team Wise Analysis":
    st.markdown("<h3>Team Wise Analysis</h3>", unsafe_allow_html=True)

    # Feature Engineering: Create a dataframe that counts the number of matches each team played in each season
    st.markdown("<h4>Matches Played by Each Team in Each Season</h4>", unsafe_allow_html=True)

    # Create a long-form dataframe for team1 and team2
    team1_df = df[['season', 'team1']].rename(columns={'team1': 'team'})
    team2_df = df[['season', 'team2']].rename(columns={'team2': 'team'})

    # Concatenate both team1 and team2 dataframes
    teams_df = pd.concat([team1_df, team2_df])

    # Group by season and team to count the number of matches played by each team in each season
    team_match_count = teams_df.groupby(['season', 'team']).size().reset_index(name='matches_played')

    # Pivot table to create a matrix of teams vs seasons (teams as rows, years as columns)
    heatmap_data = team_match_count.pivot_table(
        index='team',  # Teams on Y-axis
        columns='season',  # Years on X-axis
        values='matches_played',
        fill_value=0
    )

    # Convert all values to integers
    heatmap_data = heatmap_data.astype(int)

    # Plotting the heatmap with formatting
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues', linewidths=0.5)
    plt.title('Heatmap of Matches Played by Each Team in Each Season')
    st.pyplot()

    st.markdown("---")

    # Step 2: Most Matches Won by Each Team
    st.write("### Most Matches Won by Each Team")
    team_wins = df['winner'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Wins']

    # Plotting the bar chart of team wins
    fig = px.bar(team_wins, x='Team', y='Wins', title='Number of Matches Won by Each Team', color='Team')
    st.plotly_chart(fig)

    st.markdown("---")

    # Step 3: Team Wise Analysis (Original Part)
    # This is where we need to change the aggregation
    st.write("### Team Pair Analysis (Matches Played between Teams)")

    # Now using count of rows, since match_id doesn't exist
    team_pair_analysis = df.groupby(['team1', 'team2']).size().reset_index(name='matches_played')

    st.write(team_pair_analysis)

    # Show the first few rows of the team analysis
    st.markdown("<h4>First 5 Rows of Team Pair Analysis:</h4>", unsafe_allow_html=True)
    st.dataframe(team_pair_analysis.head())
    st.markdown("---")

    # Adding the new "Team Data" section to filter matches by teams and other parameters

    # Sidebar for team input
    st.sidebar.header("Select Teams and Match Details")

    # Select two teams from the unique teams in the dataset
    teams = sorted(set(df['team1'].unique()).union(set(df['team2'].unique())))
    team1_input = st.sidebar.selectbox("Select First Team", teams)
    team2_input = st.sidebar.selectbox("Select Second Team", teams)

    # Optional Inputs for season, match type, and venue
    selected_season = st.sidebar.selectbox("Select Season", [None] + sorted(df['season'].unique().tolist()))
    selected_match_type = st.sidebar.selectbox("Select Match Type", [None] + sorted(df['match_type'].unique().tolist()))
    selected_venue = st.sidebar.selectbox("Select Venue", [None] + sorted(df['venue'].dropna().unique().tolist()))

    # Filter data based on the user's input
    filter_condition = (
            ((df['team1'] == team1_input) & (df['team2'] == team2_input)) |
            ((df['team1'] == team2_input) & (df['team2'] == team1_input))
    )

    if selected_season:
        filter_condition &= (df['season'] == selected_season)
    if selected_match_type:
        filter_condition &= (df['match_type'] == selected_match_type)
    if selected_venue:
        filter_condition &= (df['venue'] == selected_venue)

    # Apply the filter
    filtered_matches = df[filter_condition]

    # If there are no matches, show a message
    if filtered_matches.empty:
        st.write("No matches found for the selected criteria.")
    else:
        # Display the relevant columns for match details
        st.markdown("<h4>Match Details:</h4>", unsafe_allow_html=True)
        match_details = filtered_matches[
            ['date', 'toss_winner', 'toss_decision', 'winner', 'result_margin', 'target_runs', 'target_overs',
             'super_over', 'player_of_match']]
        st.dataframe(match_details)

        # Visualizations

        # Toss Decision Distribution (Bar Plot)
        st.markdown("<h5>Toss Decision Distribution</h5>", unsafe_allow_html=True)
        toss_decision_count = filtered_matches['toss_decision'].value_counts()
        fig = px.bar(toss_decision_count, x=toss_decision_count.index, y=toss_decision_count.values,
                     labels={'y': 'Count', 'x': 'Toss Decision'}, title="Toss Decision Distribution")
        st.plotly_chart(fig)

        # Toss Winner Distribution (Bar Plot)
        st.markdown("<h5>Toss Winner Distribution</h5>", unsafe_allow_html=True)
        toss_winner_count = filtered_matches['toss_winner'].value_counts()
        fig = px.bar(toss_winner_count, x=toss_winner_count.index, y=toss_winner_count.values,
                     labels={'y': 'Count', 'x': 'Toss Winner'}, title="Toss Winner Distribution")
        st.plotly_chart(fig)

        # Match Winner Distribution (Pie Chart)
        st.markdown("<h5>Match Winner Distribution</h5>", unsafe_allow_html=True)
        match_winner_count = filtered_matches['winner'].value_counts()
        fig = px.pie(match_winner_count, names=match_winner_count.index, values=match_winner_count.values,
                     title="Match Winner Distribution")
        st.plotly_chart(fig)

        # Result Margin Distribution (Histogram)
        st.markdown("<h5>Result Margin Distribution</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(filtered_matches['result_margin'].dropna(), bins=30, color='green', edgecolor='black')
        ax.set_title("Distribution of Result Margin (Win Margin)")
        ax.set_xlabel("Result Margin")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # Target Runs Distribution (Histogram)
        st.markdown("<h5>Target Runs Distribution</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(filtered_matches['target_runs'].dropna(), bins=30, color='blue', edgecolor='black')
        ax.set_title("Distribution of Target Runs")
        ax.set_xlabel("Target Runs")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # Target Overs Distribution (Histogram)
        st.markdown("<h5>Target Overs Distribution</h5>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(filtered_matches['target_overs'].dropna(), bins=30, color='purple', edgecolor='black')
        ax.set_title("Distribution of Target Overs")
        ax.set_xlabel("Target Overs")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # Super Over Distribution (Pie Chart)
        st.markdown("<h5>Super Over Distribution</h5>", unsafe_allow_html=True)
        super_over_count = filtered_matches['super_over'].value_counts()
        fig = px.pie(super_over_count, names=super_over_count.index, values=super_over_count.values,
                     title="Super Over Distribution")
        st.plotly_chart(fig)

        # Player of the Match Distribution (Bar Plot)
        st.markdown("<h5>Player of the Match Distribution</h5>", unsafe_allow_html=True)
        player_of_match_count = filtered_matches['player_of_match'].value_counts()
        fig = px.bar(player_of_match_count, x=player_of_match_count.index, y=player_of_match_count.values,
                     labels={'y': 'Count', 'x': 'Player of Match'}, title="Player of the Match Distribution")
        st.plotly_chart(fig)

    st.markdown("---")

    # Show the first few rows of the team analysis
    st.markdown("<h4>First 5 Rows of Team Pair Analysis:</h4>", unsafe_allow_html=True)
    st.dataframe(team_pair_analysis.head())
    st.markdown("---")