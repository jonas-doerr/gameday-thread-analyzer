import streamlit as st
from analyzer import clean_comments, tokenize_comments, get_reddit_comments, find_keywords, find_most_mentioned, overall_sentiment, player_sentiments
import pandas as pd
import plotly.express as px

@st.cache_data
def load_comments(url_link, comment_depth):
    comment_list = clean_comments(get_reddit_comments(url_link, comment_depth))
    return comment_list

@st.cache_data
def lemmatization(comments):
    lemmos = tokenize_comments(comments)
    return lemmos

@st.cache_data
def comment_analysis(comments, keyword_amount, player_analysis_count):
    lemmos = tokenize_comments(comments) #lemmatize
    keywords = find_keywords(lemmos, keyword_amount) #get keywords
    keywords_df = pd.DataFrame(keywords, columns = ['Keyword', 'Count']).set_index("Keyword") #make dataframe
    win_or_lose, positive_comments, negative_comments, _ = overall_sentiment(st.session_state.cleaned_comments) #overall sentiment analysis
    _, top_players = find_most_mentioned(lemmos, player_analysis_count) #player analysis
    return keywords_df, win_or_lose, positive_comments, negative_comments, top_players

st.title("Packers Reddit Thread Analyzer")
st.write("Submit a link to a post on the GreenBayPackers subreddit and this program will analyze it!")

# Link inputs
col1, col2 = st.columns(2)
with col1:
    url_input = st.text_input("Input a Reddit Thread Link")

with col2:
    thread_presets = {"Week 2 Gameday Thread":"https://www.reddit.com/r/GreenBayPackers/comments/1neojbv/week_2_game_thread_washington_commanders_green/",
                      "Week 3 Gameday Thread":"https://www.reddit.com/r/GreenBayPackers/comments/1nmww8q/week_3_game_thread_green_bay_packers_cleveland/",
                      "Week 3 Postgame Thread":"https://www.reddit.com/r/GreenBayPackers/comments/1nn25mu/week_3_post_game_thread_green_bay_packers/",
                      "Week 2 Postgame Thread":"https://www.reddit.com/r/GreenBayPackers/comments/1nesr4u/week_2_post_game_thread_washington_commanders/"}

    thread_choice = st.selectbox("Or Choose a Preset Packers Thread", ["None"] + list(thread_presets.keys()))

if url_input:
    url = url_input.strip()
elif thread_choice != "None":
    url = thread_presets[thread_choice]
else:
    url = None

# Allows for changes in data presentation
col3, col4, col5 = st.columns(3)
with col3:
    keyword_count = st.number_input("Keywords Displayed", min_value = 1, max_value = 50, value = 10, step = 1)

with col4:
    players_analyzed = st.number_input("Players Analyzed", min_value = 1, max_value = 20, value = 5, step = 1)

with col5:
    analysis_depth = st.number_input("Analysis Depth (Impacts Speed)", min_value = 1, value = 2, step = 1)

if st.button("Analyze Data"):
    if not url:
        st.error("Please enter a Reddit thread link or choose a preset.")
    elif not url.startswith("https://www.reddit.com/r/"):
        st.error("Invalid link. Please enter a valid Reddit thread URL.")
    else:
        #Get comments and preprocess them
        st.session_state.cleaned_comments = load_comments(url, analysis_depth)

        #Run main function
        keywords_df, win_or_lose, positive_comments, negative_comments, top_players = comment_analysis(st.session_state.cleaned_comments, keyword_count, players_analyzed)

        #Find keywords
        st.subheader("Top Keywords")
        st.bar_chart(keywords_df, horizontal = True)

        #Predict win or loss
        st.subheader("Win/Loss Prediction")
        sentiment_df = pd.DataFrame({"Sentiment": ["Positive", "Negative"], "Count": [positive_comments, negative_comments]})
        sentiment_fig = px.pie(sentiment_df, names = "Sentiment", values = "Count", title = "Positive vs Negative Sentiment in Comments")
        st.plotly_chart(sentiment_fig)
        if win_or_lose is True:
            st.write("**Prediction**: It seems like the Packers won this game.")
        else:
            st.write("**Prediction**: The Packers probably lost this game.")

        # Display sentiment towards most mentioned players
        st.subheader("Sentiment Analysis of Most Mentioned Players")
        st.write("Analyzes all mentions of these players and rates the feelings towards them on a scale of 1-100. Longer bars indicate greater positivity, and a half-full bar indicates neutral sentiment.")

        #Find most mentioned players
        player_sent = player_sentiments(st.session_state.cleaned_comments, top_players)
        for player in player_sent:
            player_sent[player] = (player_sent[player] + 1) / 2 # Convert the value to fit between 0-1
            st.progress(player_sent[player], text = f"{player}")
