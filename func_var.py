import streamlit as st
import pickle
import translators as ts

games = pickle.load(open('games.pkl', 'rb'))
cosine_sim_content = pickle.load(open('cosine_sim_content.pkl', 'rb'))
cosine_sim_collab = pickle.load(open('cosine_sim_collab.pkl', 'rb'))

genres = ["Racing", "Adventure", "Sports", "Strategy", "Casual", "RPG", "Simulation", "Action", "Indie"]
games_title = games.sort_values(by='title')

# Fungsi untuk mendapatkan kesamaan content-based filtering untuk game tertentu
@st.cache_data
def get_content_based_similarities(game_idx, k):
   # Mendapatkan skor kesamaan konten untuk game_idx
   content_sim_scores = list(enumerate(cosine_sim_content[game_idx]))
   # Normalisasi skor kesamaan ke rentang 0-1
   max_content_score = max([score for _, score in content_sim_scores])
   content_sim_scores = [(idx, score / max_content_score) for idx, score in content_sim_scores]

   # Mengurutkan skor kesamaan berdasarkan nilai skor dalam urutan menurun
   sorted_content_sim_scores = sorted(content_sim_scores, key=lambda x: x[1], reverse=True)
   # Mengambil top k skor kesamaan, dimulai dari indeks 1 (skip yang pertama karena itu adalah game_id itu sendiri)
   top_content_sim_scores = sorted_content_sim_scores[1:k + 1]  # Mengambil dari indeks 1 hingga top_n+1
   # Mengembalikan daftar top k skor kesamaan konten
   return top_content_sim_scores

# Fungsi untuk mendapatkan kesamaan collaborative filtering untuk game tertentu
@st.cache_data
def get_collaborative_similarities(game_idx, k):
   # Mendapatkan skor kesamaan kolaboratif untuk game_idx
   collab_sim_scores = list(enumerate(cosine_sim_collab[game_idx]))
   
   # Normalisasi skor kesamaan ke rentang 0-1
   max_collab_score = max([score for _, score in collab_sim_scores])
   collab_sim_scores = [(idx, score / max_collab_score) for idx, score in collab_sim_scores]

   # Mengurutkan skor kesamaan berdasarkan nilai skor dalam urutan menurun
   sorted_collab_sim_scores = sorted(collab_sim_scores, key=lambda x: x[1], reverse=True)

   # Mengambil top k skor kesamaan, dimulai dari indeks 1 (skip yang pertama karena itu adalah game_id itu sendiri)
   top_collab_sim_scores = sorted_collab_sim_scores[1:k + 1]  # Mengambil dari indeks 1 hingga top_n+1
    
   # Mengembalikan daftar top k skor kesamaan kolaboratif
   return top_collab_sim_scores

# Fungsi untuk mendapatkan rekomendasi game dari content-based dan collaborative filtering
@st.cache_data
def hybrid_recommendation(input_game_title, k = 12):
   # Mendapatkan ID game untuk judul game yang diinput
   input_game_id = games[games['title'] == input_game_title]['app_id'].values[0] 
   # Mendapatkan index game untuk judul game yang diinput
   input_game_idx = games[games['app_id'] == input_game_id].index[0]
   
   # Mendapatkan skor kesamaan content-based dan collaborative
   content_sim_scores = get_content_based_similarities(input_game_idx, k)
   collab_sim_scores = get_collaborative_similarities(input_game_idx, k)
   
   # Menggabungkan skor dengan bobot yang sama (0.5)
   combined_scores = {}
   for idx, score in content_sim_scores:
       combined_scores[idx] = combined_scores.get(idx, 0) + 0.5 * score
   for idx, score in collab_sim_scores:
       combined_scores[idx] = combined_scores.get(idx, 0) + 0.5 * score
    
   # Mengurutkan game berdasarkan skor gabungan dan mengambil indeks top k game
   sorted_games = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
   recommended_game_indices = [idx for idx, _ in sorted_games[:k]]
   
   # Mengambil judul game dari indeks yang direkomendasikan
   recommended_games = games.iloc[recommended_game_indices].reset_index(drop=True)
   
   # Mengembalikan DataFrame berisi game yang direkomendasikan
   return recommended_games

# Mengurutkan DataFrame berdasarkan skor
def sorted_score_df(df):
   df['score'] = df['user_reviews'] * df['positive_ratio']
   df_sorted = df.sort_values('score', ascending=False)
   return df_sorted

@st.cache_data
def most_popular_games():
   df = games
   n = 12 #jumlah game
   list = sorted_score_df(df).reset_index(drop = True)
   return list.iloc[0:n]

def genre_filtering(list_genre = []): 
   # memfilter genre 
   df = games
   if len(list_genre) != 0:
      for genre in list_genre:
         genres_games = df[df['genres'].apply(lambda x: all(item in x for item in list_genre))]
         
      filtered_games = sorted_score_df(genres_games).reset_index(drop = True)
   else :
      filtered_games = df.sort_values('title', ascending=True).reset_index(drop = True)
   return filtered_games

@st.cache_data
def selected_game_details(game_name):
   game_id = games[games['title'] == game_name]['app_id'].values[0] 
   game_idx = games[games['app_id'] == game_id].index[0]
   list_details = games.loc[game_idx]

   title = list_details.loc['title']
   genres = list_details.loc['genres']
   tanggal = str(list_details.loc['date_release'])
   website = list_details.loc['website']
   screenshots = list_details.loc['screenshots']
   if list_details.loc['movies'] != 'Unknown':
      movies = list_details.loc['movies']
      movies = movies[0]
      movies_thumbnail = ["asset/video.jpg"]
      list_media = movies_thumbnail + screenshots
   else:
      movies = list_details.loc['movies']
      list_media = screenshots
   #text = list_details.loc['about'].split('. ')
   about = list_details.loc['about']
   #for sentence in text:
   #   trans = ts.translate_text(sentence, from_language='en', to_language='id')
   #   about = about + trans + ". "
   review = str(list_details.loc['rating'])+' ('+str(list_details.loc['user_reviews'])+')'
   developer = list_details['developers'].split(',')
   publisher = list_details['publishers'].split(',')
   header_img = list_details.loc['header_image']
   age = list_details.loc['age']
   if age == 0:
      age = 'semua usia'
   else:
      age = str(age)+'+'

   return title, genres, tanggal, website, movies, list_media, about, review, developer, publisher, header_img, age

@st.cache_data
def get_recommendation_data(game_name):
    recommendations = hybrid_recommendation(game_name)
    title, genres, tanggal, website, movies, list_media, about, review, developer, publisher, header_img, age = selected_game_details(game_name)
    return recommendations, title, genres, tanggal, website, movies, list_media, about, review, developer, publisher, header_img, age

def change_page(name):
    st.session_state['saved_name'] = name
    #st.query_params.game_name = st.session_state['saved_name']
    st.session_state['details_page'] = True
