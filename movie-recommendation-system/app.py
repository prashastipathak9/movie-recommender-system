import pickle
import streamlit as st
import pandas as pd
import requests

# Add a favicon to the app
st.set_page_config(page_title='Movie Recommender System', page_icon=':guardsman:', layout='wide')

# Define footer style
footer_style = """
    <style>
    .footer {
        font-size: 16px;
        color: white;
        position: fixed;
        bottom: 0;
        right: 0;
        left: 0;
        padding: 10px;
        text-align: center;
        background-color: #262730;
    }
    </style>
    """
st.markdown(footer_style, unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances =similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))


st.markdown("<h1 style='text-align: center'>Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
"Type or select a movie from the dropdown",
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

st.markdown('<div class="footer">Made with ❤️ by Prashasti Pathak</div>', unsafe_allow_html=True)
