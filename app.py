import streamlit as st
import pickle

import pandas as pd
import requests 

movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))  

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3a5694a9e62007b3a2329e9fb39f7c11&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:13]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_posters

st.set_page_config(page_title='Movie Recommender System', page_icon='🎥')

st.title('Hello, World!')
st.write('This is my first app in Streamlit!')

selected_movie_name = st.selectbox(
    'Which movie do you like?',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(4)
    for i, name in enumerate(recommended_movie_names):
        with cols[i % 4]:
            st.text(name)
            st.image(recommended_movie_posters[i])

