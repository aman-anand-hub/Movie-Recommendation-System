import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    responce=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=01d301d9cdc03cba1410f251639b2cd9'.format(movie_id))
    data=responce.json()
    return 'https://image.tmdb.org/t/p/original/'+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


st.title("Movie Recommender System: ")

selected_movie_name = st.selectbox('Search a movie?',movies['title'].values)

st.write('You selected:', selected_movie_name)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    container = st.container()
    cols = container.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(posters[i], use_column_width=True)
            st.caption(names[i])

