import os.path
import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np

# 경로 설정
file_path = os.path.dirname(__file__)

# 모델파일 폴더 생성
save_dir = os.path.join(file_path, 'model')

# 학습된 모델 불러오기
model_file = 'mnist_model.h5'
model = load_model(os.path.join(save_dir, model_file))

# 헤더 출력
st.subheader('손글씨 숫자 인식')

# 이미지 파일 업로드
img_file = st.file_uploader('Upload Images', type=['png', 'jpg', 'jpeg', 'bmp'])
if img_file is not None:
    # 업로드 이미지 출력
    img = Image.open(img_file)
    img_resize = img.resize((28,28))
    st.image(img_resize, width=200)

    st.subheader('모델이 인식한 숫자')

    # 이미지 인식
    img_resize = np.asarray(img_resize)
    #print(img_resize)
    #print(img_resize.shape)
    res = model.predict(np.reshape(img_resize, (1, 28 * 28)))
    st.success(np.argmax(res[0]))
