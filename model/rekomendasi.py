import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    profil_df = pd.read_excel('data/profil_dataset.xlsx')
    penanganan_df = pd.read_excel('data/penanganan_dataset.xlsx')

    # Preprocessing
    for col in ['keluhan_inti', 'rekomendasi_medis', 'rekomendasi_non_medis', 'profil_pengguna']:
        profil_df[col] = profil_df[col].astype(str).str.lower()

    penanganan_df['keluhan_inti'] = penanganan_df['keluhan_inti'].astype(str).str.lower()
    penanganan_df['penanganan'] = penanganan_df['penanganan'].astype(str).str.lower()

    stop_words = [
        'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 'atau',
        'ini', 'itu', 'juga', 'karena', 'agar', 'bagi', 'dalam', 'saat', 'setelah',
        'sebelum', 'tidak', 'bisa', 'ada', 'adalah', 'akan', 'oleh', 'mempunyai',
        'sebagai', 'lebih'
    ]

    tfidf_keluhan = TfidfVectorizer(stop_words=stop_words)
    tfidf_keluhan_matrix = tfidf_keluhan.fit_transform(profil_df['keluhan_inti'])

    return profil_df, penanganan_df, tfidf_keluhan, tfidf_keluhan_matrix

def hybrid_recommend(user_keluhan, user_profil, tfidf_keluhan, tfidf_keluhan_matrix, train_df, penanganan_df, top_n=3):
    user_vec = tfidf_keluhan.transform([user_keluhan.lower()])
    similarity = cosine_similarity(user_vec, tfidf_keluhan_matrix).flatten()
    top_indices = similarity.argsort()[-top_n:][::-1]

    hasil = train_df.iloc[top_indices][[
        'keluhan_inti', 'profil_pengguna', 'rekomendasi_medis', 'rekomendasi_non_medis'
    ]].copy()
    hasil['similarity_score'] = similarity[top_indices]

    hasil_medis = penanganan_df[
        penanganan_df['keluhan_inti'].isin(hasil['keluhan_inti'])
    ][['keluhan_inti', 'penanganan']].drop_duplicates()

    hasil_final = hasil.merge(hasil_medis, on='keluhan_inti', how='left')

    # Pastikan hanya 3 teratas saja yang dikirim ke template
    return hasil_final.head(3).to_dict(orient='records')
