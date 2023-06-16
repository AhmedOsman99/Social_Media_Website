from mainpro import app

# instead of using FLASK_DEBUG=1 -> python start.py
if __name__ == '__main__':
    app.run(debug=True)