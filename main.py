from flask import Flask, request, render_template
from model import calculate_words_vec, get_most_similar
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/new')
def new():
  return render_template('new.html')

@app.route('/show',methods=['GET',"POST"])
def result():
  if request.method == 'GET':
    return render_template('new.html')
  elif request.method == 'POST':
    char = request.form.getlist("character")
    ideal = request.form.getlist("ideal")
    key_list = char + ideal
    emothion_vector = calculate_words_vec(key_list)
    max_genre, max_score = get_most_similar(emothion_vector)
    return render_template("show.html", max_genre = max_genre)

if __name__ == "__main__":
  app.run()
