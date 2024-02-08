import streamlit as st 
import pandas as pd
import numpy as np
import pickle as pk
import requests

movies_dict=pk.load(open('movie_dict.pkl', 'rb'))
new_df=pd.DataFrame(movies_dict)

cosine_sim=pk.load(open('cosine_sim.pkl', 'rb'))


def fetch_posters(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=cosine_sim[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key= lambda x: x[1])[1:6]
    recommanded_movie=[]
    recommanded_movie_posters=[]
    for i in movie_list:
        movie_id=i[0]
        #fetch poster from API  server
        recommanded_movie.append(new_df.iloc[i[0]].title)
        movie_id=new_df.iloc[i[0]].movie_id
        recommanded_movie_posters.append(fetch_posters(movie_id))
    return recommanded_movie,recommanded_movie_posters

st.title('Movie Recommender System')

selected_movie=st.selectbox('Choose your Movie',new_df['title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        # st.header(names[0])
        st.image(posters[0], width=135, caption=names[0])
    with col2:        
        st.image(posters[1], width=135, caption=names[1])
    with col3:
        st.image(posters[2], width=135, caption=names[2])
    with col4:
        st.image(posters[3], width=135, caption=names[3])
    with col5:
        st.image(posters[4], width=135, caption=names[4])



            

