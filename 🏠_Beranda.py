# Mengimpor library Streamlit untuk membangun antarmuka web
import streamlit as st
# Mengimpor modul kustom dari file bernama func_var.py
from func_var import games_title, most_popular_games
# Mengatur konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Beranda", # Judul halaman
    page_icon="🏠", # Ikon halaman
    layout="wide", # Layout diatur ke "wide" untuk tampilan lebar
    initial_sidebar_state="auto" # Sidebar diatur untuk terbuka otomatis
)
# Menampilkan judul utama
st.title("Aplikasi Rekomendasi Game")
st.divider()
# Membuat wadah untuk search box
con = st.container(border=True)
con.markdown('Pencarian rekomendasi game')
# Membagi wadah menjadi dua kolom dengan rasio 3:1
col1, col2 = con.columns([3,1])
with col1:
    # Membuat kotak pilihan (selectbox) yang berisi daftar judul game dari games_title['title']
    # Pengguna dapat memilih atau mengetikkan judul game
    selected_game = st.selectbox(
        "Type or select a game",
        games_title['title'],
        index = None,
        placeholder = "Ketik atau pilih game",
        label_visibility = "collapsed")
with col2:
    # Membuat tombol "Cari rekomendasi"
    if st.button('Cari rekomendasi', use_container_width=True):
        # Jika tomblo diklik maka judul game akan disimpan pada query URL
        # dan halaman akan beralih ke halaman rekomendasi game
        st.session_state['saved_name'] = selected_game
        st.switch_page("pages/🎮_Rekomendasi_Game.py")
# Game Terpopuler
# Membuat wadah untuk menampilkan game terpopuler
with st.container(border=True):
    st.markdown("Game terpopuler")
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)
    # Memanggil fungsi most_popular_games() untuk mendapatkan daftar game terpopuler
    list_popular = most_popular_games()
    # Loop untuk menampilkan game terpopuler
    index = 0
    for col in row1 + row2 + row3 + row4:
        image = list_popular.loc[index,'header_image']
        title = list_popular.loc[index,'title']
        cont = col.container(border = True)
        cont.image(image)
        # Membuat tombol untuk beralih ke halaman rekomendasi game
        # sesuai dengan judul game yang dipilih
        if cont.button(title, use_container_width = True):
            st.session_state['saved_name'] = title
            st.switch_page("pages/🎮_Rekomendasi_Game.py")
        index = index + 1

