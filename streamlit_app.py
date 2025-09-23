import streamlit as st
from analyzer import clean_comments, tokenize_comments, get_reddit_comments, find_keywords, find_most_mentioned, overall_sentiment, player_sentiments
import pandas as pd

st.title("Packers Reddit Thread Analyzer")
st.write("Submit a link to a post on the GreenBayPackers subreddit and this program will analyze it!")
st.write(f"Here's a few options to get you started:\nhttps://www.reddit.com/r/GreenBayPackers/comments/1neojbv/week_2_game_thread_washington_commanders_green/\nhttps://www.reddit.com/r/GreenBayPackers/comments/1nmww8q/week_3_game_thread_green_bay_packers_cleveland/\nhttps://www.reddit.com/r/GreenBayPackers/comments/1nn25mu/week_3_post_game_thread_green_bay_packers/\nhttps://www.reddit.com/r/GreenBayPackers/comments/1nesr4u/week_2_post_game_thread_washington_commanders/")

col1, col2 = st.columns(2)
with col1:
    url = st.text_input("reddit thread link")

with col2:
    pass

if st.button("Analyze Data") and url:
    #Get comments and preprocess them
    st.session_state.cleaned_comments = clean_comments(get_reddit_comments(url, 2))

    #Lemmatize comments
    st.session_state.lemmatized_comments = tokenize_comments(st.session_state.cleaned_comments)

    #Find keywords
    st.subheader("Top Keywords")
    keywords = find_keywords(st.session_state.lemmatized_comments, 10)
    keywords_df = pd.DataFrame(keywords, columns = ['Keyword', 'Count']).set_index("Keyword")
    st.bar_chart(keywords_df, horizontal = True)

    #Predict win or loss
    st.subheader("Win/Loss Prediction")
    win_or_lose, _, _, _ = overall_sentiment(st.session_state.cleaned_comments)
    if win_or_lose is True:
        st.write("It seems like the Packers won this game.")
    else:
        st.write("The Packers probably lost this game.")

    # Display sentiment towards most mentioned players
    st.subheader("Sentiment Analysis of Most Mentioned Players")
    st.write("Analyzes all mentions of these players and rates the feelings towards them on a scale of 1-100. Longer bars indicate greater positivity, and a half-full bar indicates neutral sentiment.")

    #Find most mentioned players
    mentioned_player, top_players = find_most_mentioned(st.session_state.lemmatized_comments, 5)

    player_sent = player_sentiments(st.session_state.cleaned_comments, top_players)
    for player in player_sent:
        player_sent[player] = (player_sent[player] + 1) / 2 # Convert the value to fit between 0-1
        st.progress(player_sent[player], text = f"{player}")
    # player_sent_df = pd.DataFrame(list(player_sent.items()), columns = ["Player", "Sentiment"])
    # st.progress(player_sent_df)


