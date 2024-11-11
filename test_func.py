import pytest
import pandas as pd

# Mock data untuk Dataframe games, matriks cosine_sim_content dan cosine_sim_collab
mock_games = pd.DataFrame({
    'title': ['Game1', 'Game2', 'Game3', 'Game4'],
    'app_id': [1, 2, 3, 4],
    'genres': [['Action'], ['Adventure'], ['RPG'], ['Action', 'RPG']],
    'user_reviews': [100, 150, 200, 250],
    'positive_ratio': [0.9, 0.85, 0.95, 0.88],
    'date_release': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01'],
    'website': ['http://game1.com', 'http://game2.com', 'http://game3.com', 'http://game4.com'],
    'screenshots': [['shot1.png'], ['shot2.png'], ['shot3.png'], ['shot4.png']],
    'movies': [['movie1.mp4'], 'Unknown', ['movie3.mp4'], ['movie4.mp4']],
    'about': ['About Game1', 'About Game2', 'About Game3', 'About Game4'],
    'rating': [4.5, 4.0, 4.7, 4.2],
    'developers': ['Dev1', 'Dev2', 'Dev3', 'Dev4'],
    'publishers': ['Pub1', 'Pub2', 'Pub3', 'Pub4'],
    'header_image': ['header1.png', 'header2.png', 'header3.png', 'header4.png']
})
mock_cosine_sim_content = [
    [1.0, 0.8, 0.6, 0.4],
    [0.8, 1.0, 0.7, 0.3],
    [0.6, 0.7, 1.0, 0.2],
    [0.4, 0.3, 0.2, 1.0]
]
mock_cosine_sim_collab = [
    [1.0, 0.5, 0.4, 0.3],
    [0.5, 1.0, 0.6, 0.2],
    [0.4, 0.6, 1.0, 0.1],
    [0.3, 0.2, 0.1, 1.0]
]
# Fixture untuk mengganti variabel global
@pytest.fixture
def setup_mocks(monkeypatch):
    # Mengganti file pickle yang dimuat dengan data mock
    monkeypatch.setattr('pickle.load', lambda f: mock_games if 'games.pkl' in f.name else mock_cosine_sim_content if 'cosine_sim_content.pkl' in f.name else mock_cosine_sim_collab)
# TEST CASE 1|Pengujian fungsi get_content_based_similarities positif
def test_get_content_based_similarities(setup_mocks):
    from func_var import get_content_based_similarities
    result = get_content_based_similarities(0, 2)
    expected = [(1, 0.8), (2, 0.6)]
    assert result == expected
# TEST CASE 2|Pengujian fungsi get_content_based_similarities negatif
def test_get_content_based_similarities_invalid_index(setup_mocks):
    from func_var import get_content_based_similarities
    with pytest.raises(IndexError):
        get_content_based_similarities(10, 2)
# TEST CASE 3|Pengujian fungsi get_collaborative_similarities positif
def test_get_collaborative_similarities(setup_mocks):
    from func_var import get_collaborative_similarities
    result = get_collaborative_similarities(0, 2)
    expected = [(1, 0.5), (2, 0.4)]
    assert result == expected
# TEST CAE 4|Pengujian fungsi get_collaborative_similarities negatif
def test_get_collaborative_similarities_invalid_index(setup_mocks):
    from func_var import get_collaborative_similarities
    with pytest.raises(IndexError):
        get_collaborative_similarities(10, 2)
# TEST CASE 5|Pengujian fungsi hybrid_recommendation positif
def test_hybrid_recommendation(setup_mocks):
    from func_var import hybrid_recommendation
    result = hybrid_recommendation('Game1', 2)
    expected_titles = ['Game2', 'Game3']
    assert result['title'].tolist() == expected_titles
# TEST CASE 6|Pengujian fungsi hybrid_recommendation negatif
def test_hybrid_recommendation_invalid_title(setup_mocks):
    from func_var import hybrid_recommendation
    with pytest.raises(IndexError):
        hybrid_recommendation('NonExistentGame', 2)
# TEST CASE 7|Pengujian fungsi hybrid_recommendation negatif
def test_hybrid_recommendation_invalid_k(setup_mocks):
    from func_var import hybrid_recommendation
    result = hybrid_recommendation('Game1', -1)
    assert result.empty
# TEST CASE 8|Pengujian fungsi sorted_score_df positif    
def test_sorted_score_df(setup_mocks):
    from func_var import sorted_score_df, games
    result = sorted_score_df(games)
    expected_titles = ['Game4', 'Game3', 'Game2', 'Game1']
    assert result['title'].tolist() == expected_titles
    assert 'score' in result.columns
# TEST CASE 9|Pengujian fungsi sorted_score_df negatif   
def test_sorted_score_df_empty(setup_mocks):
    from func_var import sorted_score_df
    empty_df = pd.DataFrame(columns=['title', 'user_reviews', 'positive_ratio'])
    result = sorted_score_df(empty_df)
    assert result.empty
# TEST CASE 10|Pengujian fungsi genre_filtering positif  
def test_genre_filtering_single_genre(setup_mocks):
    from func_var import genre_filtering
    result = genre_filtering(['Action'])
    expected_titles = ['Game4', 'Game1']
    assert result['title'].tolist() == expected_titles
# TEST CASE 11|Pengujian fungsi genre_filtering positif  
def test_genre_filtering_multiple_genres(setup_mocks):
    from func_var import genre_filtering
    result = genre_filtering(['Action', 'RPG'])
    expected_titles = ['Game4']
    assert result['title'].tolist() == expected_titles
# TEST CASE 12|Pengujian fungsi genre_filtering positif  
def test_genre_filtering_no_genre(setup_mocks):
    from func_var import genre_filtering
    result = genre_filtering([])
    expected_titles = ['Game1', 'Game2', 'Game3', 'Game4']
    assert result['title'].tolist() == expected_titles
# TEST CASE 13|Pengujian fungsi genre_filtering negatif  
def test_genre_filtering_non_existent_genre(setup_mocks):
    from func_var import genre_filtering
    result = genre_filtering(['NonExistent'])
    assert result.empty
# TEST CASE 14|Pengujian fungsi selected_game_details positif  
def test_selected_game_details_valid(setup_mocks):
    from func_var import selected_game_details
    result = selected_game_details('Game1')
    expected = (
        'Game1',
        ['Action'],
        '2022-01-01',
        'http://game1.com',
        'movie1.mp4',
        ['asset/video.jpg', 'shot1.png'],
        'About Game1',
        '4.5 (100)',
        ['Dev1'],
        ['Pub1'],
        'header1.png'
    )
    assert result == expected
# TEST CASE 15|Pengujian fungsi selected_game_details positif  
def test_selected_game_details_no_movie(setup_mocks):
    from func_var import selected_game_details
    result = selected_game_details('Game2')
    expected = (
        'Game2',
        ['Adventure'],
        '2022-02-01',
        'http://game2.com',
        'Unknown',
        ['shot2.png'],
        'About Game2',
        '4.0 (150)',
        ['Dev2'],
        ['Pub2'],
        'header2.png'
    )
    assert result == expected
# TEST CASE 16|Pengujian fungsi selected_game_details negatif
def test_selected_game_details_invalid_game(setup_mocks):
    from func_var import selected_game_details
    with pytest.raises(IndexError):
        selected_game_details('NonExistentGame') 