from flask import (Flask, render_template)
import connexion
import config


connex_app = config.connex_app
# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# Create a URL route in our application for "/"
@connex_app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    connex_app.run(debug=True, port=5000)
