from server import app

def main():    
    app.run(debug=True, port=5001, host='0.0.0.0')


main()