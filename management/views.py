from management import app


@app.route('/')
def index():
    return 'Hello Store managemenet!!!'
