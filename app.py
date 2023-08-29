import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '58c98a24ccee35cbe9d684cc651152fc'
tmdb.language = 'ko-KR' # movie를 통해 가져오는 데이터가 모두 한국 기준

def get_recommendations(title):
    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
    idx = movies[movies['title'] == title].index[0]

    # 코사인 유사도 메트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # (idx, 유사도, 내림차순)

    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:11] # 0 은 자기자신
        
    # 추천 영화 목록 10개의 인덱스 정보 추출
    movie_indices = [i[0]  for i in sim_scores]
        
    # 인덱스 정보를 통해 영화 제목을 추출
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)

        image_path = details['poster_path']
        # 이미지가 없는 영화목록을 불러올때 에러가 뜨는 상황 보안
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title'])

    return images, titles

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

# 전체화면 설정
st.set_page_config(layout='wide')

# 화면 상단의 제목역할
st.header('KHflix')

# 영화목록 다 꺼내서 콤보박스 형태로 만들기
movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
# 버튼 동작
if st.button('Recommend'):
    with st.spinner('Please wait...'): # 찾는중인 대기시간일 때 화면이 공백인것을 보안
        images, titles = get_recommendations(title)

        idx = 0 # 10 개의 image, title을 가져와서 0번째, 1번째,...
        for i in range(0, 2): # 2 줄 만들기
            cols = st.columns(5) # 5 개의 컬럼을 만들기
            for col in cols: # 각 컬럼을 반복
                col.image(images[idx]) # 각 컬럼의 이미지
                col.write(titles[idx]) # 각 컬럼의 제목
                idx += 1 # idx를 더해줘서 다음 idx의 정보를 가져오기