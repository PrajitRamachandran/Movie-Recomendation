from flask import Flask, render_template, request
from recom import recommend

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def get_recommendation():
    movie = request.form.get('movie_input')  # ✅ safe access

    if not movie:
        return render_template('index.html', recommendations=[])

    results = recommend(movie)

    return render_template('index.html', recommendations=results)


if __name__ == '__main__':
    app.run(debug=True)