import json

from flask import render_template, request

from analytics import get_keywords_recomendations
from config import app


@app.route('/')
def home():
    return render_template('home.html', data="This is data")

@app.route('/precision-test/')
def precision():
    return render_template('precision_test.html', data="This is data")

@app.route('/api/analytics/')
def analytics_api():
    keyword = request.args.get('q')
    recomendation_rdd = get_keywords_recomendations(keyword)
    result = recomendation_rdd.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(result)

@app.route('/api/precision/')
def precision_api():
    keyword = request.args.get('q')
    return json.dumps(get_precision_test(keyword))

if __name__ == '__main__':
    app.run()
