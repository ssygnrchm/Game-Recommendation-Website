# Mengimpor library Streamlit untuk membuat UI web
import streamlit as st
# Mengimpor komponen-komponen UI dari Ant Design untuk Streamlit
import streamlit_antd_components as sac
# Mengimpor fungsi-fungsi dan variabel dari file func_var.py
# untuk keperluan filtering berdasarkan genre, data genre, dan mengubah halaman.
from func_var import genre_filtering, genres, change_page
# Mengatur konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Katalog Game",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="auto"
)
# Memeriksa apakah variabel details_page ada dalam sesi pengguna  
if 'details_page' not in st.session_state :
  st.session_state['details_page'] = False
if st.session_state['details_page'] == True:
  # Jika halaman detail game aktif (details_page bernilai True),
  # maka variabel details_page diatur ke False 
  # dan halaman dialihkan ke halaman rekomendasi game
  st.session_state['details_page'] = False
  st.switch_page("pages/🎮_Rekomendasi_Game.py")
# Mendeklarasikan fungsi show_data 
# yang menampilkan data game di halaman berdasarkan indeks yang diberikan  
def show_data(index):
  # Membagi setiap baris (row1-row5) menjadi 3 kolom (col)
  # untuk menampilkan game dalam format grid
  a = row1.columns(3)
  b = row2.columns(3)
  c = row3.columns(3)
  d = row4.columns(3)
  e = row5.columns(3)
  if 'index' not in st.session_state:
    st.session_state['index'] = str(index)
  for col in a + b + c + d + e :
    if index < len(list_popular):
      cont = col.container(border = True)
      title = list_popular.loc[index,'title']
      # Menampilkan gambar header game
      cont.image(list_popular.loc[index,'header_image'])
      # Menampilkan tombol dengan judul game. 
      # Jika tombol diklik, fungsi change_page akan dipanggil dengan argumen title
      # untuk mengubah halaman ke halaman detail game
      if cont.button(title, use_container_width = True):
        st.session_state['saved_name'] = title
        st.switch_page("pages/🎮_Rekomendasi_Game.py")
        #cont.button(title, on_click = change_page, args = [title], use_container_width = True)
      index = index + 1
    else :
      # Jika indeks sudah tidak valid (melebihi jumlah game), maka iterasi berhenti
      break 
  # Memperbarui nilai index dalam session state
  st.session_state['index'] = str(index)
# Tampilan Katalog Game
# Menampilkan judul halaman
st.title("Katalog Game")

if 'list_genre' not in st.session_state :
  st.session_state['list_genre'] = []
else:
  if 'temp_list_genre' in st.session_state:
    st.session_state.list_genre = st.session_state.temp_list_genre
# Membuat komponen multiselect untuk memilih genre
genre_options = st.multiselect(
  "What are your favorite colors",
  options = genres,
  key = "temp_list_genre",
  default = st.session_state['list_genre'],
  placeholder = "Pilih genre game yang diinginkan",
  label_visibility = "collapsed",
)
# Menyimpan pilihan genre yang dipilih oleh pengguna ke dalam session state
st.session_state['list_genre'] = genre_options
# Memanggil fungsi genre_filtering untuk memfilter game berdasarkan genre yang dipilih
list_popular = genre_filtering(st.session_state['list_genre'])
# Menghitung jumlah game yang telah difilter
total_game = len(list_popular)
# Membuat wadah dengan border untuk menampilkan grid game
with st.container(border=True):
  # Membuat lima baris (row1-row5) kosong yang akan diisi dengan konten game nanti
  row1 = st.empty()
  row2 = st.empty()
  row3 = st.empty()
  row4 = st.empty()
  row5 = st.empty()
# Membuat komponen pagination untuk mengatur navigasi halaman
pagination = sac.pagination(total=total_game, page_size=15, align='center', variant='filled', simple=True,)
# Mendapatkan nomor halaman aktif dari komponen pagination
x = int(pagination)
# Menghitung indeks awal untuk menampilkan game pada halaman aktif
index = (15*x)-15
# Memanggil fungsi show_data untuk menampilkan 15 game dari 
# indeks awal yang dihitung pada langkah sebelumnya
show_data(index)
