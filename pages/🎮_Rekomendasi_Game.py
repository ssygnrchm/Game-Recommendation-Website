# Mengimpor library Streamlit untuk membuat antarmuka web (UI)
import streamlit as st
# Mengimpor komponen-komponen UI dari Ant Design untuk Streamlit
import streamlit_antd_components as sac
# Mengimpor komponen untuk memilih gambar
from streamlit_image_select import image_select
# Mengimpor variabel dan fungsi dari file func_var.py 
# untuk keperluan penanganan genre, mendapatkan data rekomendasi, 
# dan mengubah halaman
from func_var import genres, get_recommendation_data, change_page
# Mengatur konfigurasi halaman
st.set_page_config(
    page_title="Rekomendasi Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="auto"
)
# Untuk mengalihkan halaman ke halaman katalog game jika ada genre yang dipilih
if 'selected_genre' in st.session_state and st.session_state.selected_genre in genres:
    st.session_state.list_genre = st.session_state.selected_genre
    st.switch_page("pages/📃_Katalog_Game.py")
# Mendeklarasikan fungsi untuk menampilkan daftar game rekomendasi dalam format grid 4x3
def view_list(data):
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)
    # Loop untuk menampilkan game pada setiap kolom
    index = 0
    for col in row1 + row2 + row3 + row4:
        cont = col.container(border = True)
        cont.image(data.loc[index,'header_image'], use_column_width = True)
        title = data.loc[index,'title']
        genres = data.loc[index, 'genres']
        review = str(data.loc[index, 'rating'])+' ('+str(data.loc[index, 'user_reviews'])+')'
        age = data.loc[index, 'age']
        if age == 0:
            age = 'semua usia'
        else:
            age = str(age)+'+'
        # Membuat popover (tooltip) yang muncul saat mengarahkan kursor ke judul game
        popover = cont.popover(title, use_container_width = True)
        cols1 = popover.columns([1, 3])
        cols2 = popover.columns([1, 3])
        cols3 = popover.columns([1, 3])
        # Menampilkan genre game
        cols1[0].markdown("Genre")
        with cols1[1] :
            sac.tags(genres, format_func='title', key=index)
        # Menampilkan review game
        cols2[0].markdown("Review")
        cols2[1].markdown(review)
        cols3[0].markdown("Usia")
        cols3[1].markdown(age)
        # Menambahkan tombol "more..." di dalam popover 
        # yang akan mengarahkan pengguna ke halaman rekomendasi game saat diklik
        popover.button("lebih banyak...", on_click = change_page, args = [title], use_container_width = True, key=str("btn_more_"+str(index)))

        index = index + 1
# Mendeklarasikan fungsi untuk menampilkan detail game yang dipilih
def detail_selected_game(title, genres, tanggal, website, movies, list_media, about, review, developer, publisher, header_img, age):
    con = st.container(border = True)
    # Membuat container utama dan membagi menjadi 2 kolom
    cols_con = con.columns([3, 2])
    # Kolom kiri:
    # - Menampilkan media (gambar atau video) dari game.
    # - Menampilkan expander "Gallery" untuk memilih gambar atau video lain.
    # - Menampilkan expander "About the game" dengan deskripsi game
    with cols_con[0]:
        if 'media_url' not in st.session_state or 'temp_url' not in st.session_state or st.session_state.temp_url == None:
            media_idx = 0
            st.session_state['media_url'] = list_media[media_idx]
        else :
            media_idx = st.session_state['temp_url']
            url = list_media[st.session_state['temp_url']]
            st.session_state['media_url'] = url

        with st.container(border = True):
            placeholder_media = st.empty()
            if movies != 'Unknown' and media_idx == 0:
                placeholder_media.video(movies)
            elif media_idx > 0:
                placeholder_media.image(st.session_state['media_url'], use_column_width = True)
        with st.container(height= 530, border = False):
            with st.expander("**Galeri**", expanded = True):
                with st.container(height=400, border=False):
                    img = image_select(label = "", images = list_media, key="temp_url", return_value="index")
            with st.expander("**Tentang game**") :
                with st.container(height=400, border=False):
                    st.markdown(about)
    # Kolom kanan:
    # - Menampilkan header image, judul, genre, rating, tanggal rilis, website, developer, dan publisher dari game                
    with cols_con[1].container(border=True):
        st.image(header_img, use_column_width = True)
        st.html("<h2 style='text-align: center;'>"+title+"</h2>")
        with st.container(height=600,border=False):
            sac.divider(label='Genre', align='center', color='gray')
            sac.buttons(genres, label='', index=None, align='center', size='sm', radius='lg', gap='sm', variant='filled', color='dark', use_container_width=True, key='selected_genre')
            sac.divider(label='Reviews', align='center', color='gray')
            st.html("<p style='text-align: center;'>"+review+"</p>")
            sac.divider(label='Batasan Usia', align='center', color='gray')
            st.html("<p style='text-align: center;'>"+age+"</p>")
            sac.divider(label='Tanggal Rilis', align='center', color='gray')
            st.html("<p style='text-align: center;'>"+tanggal+"</p>")
            if website != 'Unknown':
                sac.divider(label='Website', align='center', color='gray')
                st.html("<p style='text-align: center;'><a href=\""+website+"\" target=\"_blank\">🌎 "+website+"</a></p>")
            sac.divider(label='Developer', align='center', color='gray')
            sac.buttons(developer, label='', index=None, align='center', size='sm', radius='lg', gap='sm', variant='filled', color='dark', use_container_width=True, key='dev')
            if publisher != 'Unknown':
                sac.divider(label='Publisher', align='center', color='gray')
                sac.buttons(publisher, label='', index=None, align='center', size='sm', radius='lg', gap='sm', variant='filled', color='dark', use_container_width=True, key='pub')
# Mendeklarasikan fungsi untuk menampilkan detail dan rekomendasi game berdasarkan nama game
def view(game_name):
    # Mendapatkan data rekomendasi dan detail game dari fungsi get_recommendation_data
    data, title, genres, tanggal, website, movies, list_media, about, review, developer, publisher, header_img, age = get_recommendation_data(game_name)
    # Menampilkan header
    st.header("Detail Game")
    # Memanggil fungsi detail_selected_game untuk menampilkan detail game
    detail_selected_game(title, genres, tanggal, website, movies, list_media, about, review, developer, publisher, header_img, age)
    # # Menampilkan header
    st.header("Daftar Rekomendasi Game")
    # Memanggil fungsi view_list untuk menampilkan daftar game rekomendasi
    view_list(data)

if 'details_page' not in st.session_state :
    st.session_state['details_page'] = False
elif st.session_state['details_page'] == True:
    st.session_state['details_page'] = False
    st.switch_page("pages/🎮_Rekomendasi_Game.py")

if "game_name" in st.query_params:
    # Mengambil nama game dari parameter
    game_name = st.query_params.game_name
    # Menyimpan nama game ke dalam session state
    st.session_state['saved_name'] = game_name
    # Menampilkan detail dan rekomendasi game
    view(game_name)
else:
    # Memeriksa apakah terdapat nama game yang disimpan di session state
    if 'saved_name' in st.session_state:
        # Jika ada, tampilkan detail dan rekomendasi game berdasarkan nama game tersebut
        game_name = st.session_state['saved_name']
        view(game_name)
    else:
        # Jika tidak ada, 
        # tampilkan pesan peringatan untuk memilih game terlebih dahulu 
        # dan berikan tautan kembali ke halaman Beranda atau Katalog Game
        with st.container(border = True):
            st.header('🔴 PILIH GAME TERLEBIH DAHULU 🔴')
            st.page_link("🏠_Beranda.py", label="Beranda", icon="🏠", use_container_width = True)
            st.page_link("pages/📃_Katalog_Game.py", label="Katalog Game", icon="📃", use_container_width = True)