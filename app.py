import json

from flask import render_template, request

from analytics import get_keywords_recomendations
from config import app


@app.route('/')
def home():
    return render_template('home.html', data="This is fucking data")

@app.route('/api/analytics/')
def analytics_api():
    keyword = request.args.get('q')
    recomendation_rdd = get_keywords_recomendations(keyword)
    result = recomendation_rdd.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
