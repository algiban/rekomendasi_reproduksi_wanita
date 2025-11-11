from flask import Flask, render_template, request
from model.rekomendasi import hybrid_recommend, load_data

app = Flask(__name__)

# Load dataset saat server dijalankan
train_df, penanganan_df, tfidf_keluhan, tfidf_keluhan_matrix = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hasil', methods=['POST'])
def hasil():
    usia = request.form['usia']
    profil = request.form['profil']
    keluhan = request.form['keluhan']

    user_profil = f"{usia}, {profil}"
    hasil = hybrid_recommend(keluhan, user_profil, tfidf_keluhan, tfidf_keluhan_matrix, train_df, penanganan_df)

    return render_template('result.html', hasil=hasil, keluhan=keluhan, profil=user_profil)

app = app 
