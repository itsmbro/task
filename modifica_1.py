import streamlit as st
import random

def get_random_sentence():
    sentences = ["Hello, world!", "Python is awesome", "Streamlit makes coding interactive", "Let's code something cool today!"]
    return random.choice(sentences)

if st.button('Generate Random Sentence'):
    st.write(get_random_sentence())