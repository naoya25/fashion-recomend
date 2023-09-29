from sentence_transformers import util, SentenceTransformer
import scipy.spatial.distance
import pandas as pd
import numpy as np

def calculate_words_vec(words):
  model = SentenceTransformer('stsb-xlm-r-multilingual')

  embeddings = model.encode(words, convert_to_tensor=True)
  avg_embedding = np.mean(np.array(embeddings), axis=0, dtype=np.float32)
  return avg_embedding.tolist()

def get_most_similar(words_vec):
  df = pd.read_csv('./static/csv/wear.csv')
  max_score = 0
  for gname in set(df['genre']):
    genre_bodies = df.query("genre == @gname")['body'].tolist()
    vec = calculate_words_vec(genre_bodies)
    score = 1-scipy.spatial.distance.cosine(words_vec, vec)
    if score > max_score:
      max_genre = gname
      max_score = score
  return max_genre, max_score

print(get_most_similar(calculate_words_vec(['楽しい', '嬉しい'])))
