from flask import Flask, request, jsonify, redirect, url_for
import requests
import urllib.parse

app = Flask(__name__)


# Function to get the Facebook login URL
def get_facebook_login_url(client_id):
    """
    Input :   client_id: The ID of the Facebook app.
    Output:   Returns the URL for Facebook login.
    """
    # Initialize the parameters
    params = {
        "client_id": client_id,
        "redirect_uri": url_for('facebook_callback_route', _external=True),
        "scope": "user_photos, publish_to_groups",
        "response_type": "code"
    }

    # Generating the facebook login url
    login_url = "https://www.facebook.com/v12.0/dialog/oauth?" + urllib.parse.urlencode(params)
    return login_url


# Function to exchange the authorization code for an access token
def exchange_code_for_access_token(code, client_id, client_secret):
    """
    Input:   code: The authorization code returned by Facebook.
             client_id: The ID of the Facebook app.
             client_secret: The secret key of the Facebook app.
    Output:  The access token returned by Facebook.
    """

    token_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": url_for('facebook_callback_route', _external=True),
        "code": code
    }

    response = requests.get("https://graph.facebook.com/v12.0/oauth/access_token", params=token_params)
    #print(response)
    #print(response.json().get('access_token'))
    return response.json().get('access_token')


# Function to share a photo on Facebook
def share_photo_on_facebook(access_token, photo_url):
    """
    Shares a photo on Facebook using the provided access token.
    Input:    access_token: The access token to use for sharing the photo.
              photo_url: The URL of the photo to be shared on Facebook.
    Output:   The response returned by Facebook.
    """

    params = {
        "url": photo_url,
        "access_token": access_token
    }

    response = requests.post("https://graph.facebook.com/v12.0/me/photos", params=params)

    return response.json()


# Function to handle the Facebook callback
def facebook_callback():
    """
    Handles the Facebook callback after a user logs in.
    """
    client_id = '<Facebook-app-id>'
    client_secret = '<Facebook-app-secret>'
    photo_url = 'https://cdn.pixabay.com/photo/2013/07/18/10/56/railroad-163518_960_720.jpg'
    
    
    # The authorization code returned by Facebook
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    access_token = exchange_code_for_access_token(code, client_id, client_secret)

    # Share the photo on Facebook using the access token
    share_response = share_photo_on_facebook(access_token, photo_url)

    if share_response.get('error'):
        return jsonify({'status': 'error', 'message': 'Error sharing photo on Facebook'})
    else:
        return jsonify({'status': 'success', 'message': 'Photo shared successfully on Facebook'})


# Define a new route to handle the Facebook callback
@app.route('/facebook-callback')
def facebook_callback_route():
    """
    Route for handling the Facebook callback.
    """
    return facebook_callback()


# Define a new route to generate the Facebook login URL
@app.route('/get-facebook-login-url')
def get_facebook_login_url_route():
    """
    Route for generating the Facebook login URL.
    """
    client_id = '<Facebook-app-id>'
    login_url = get_facebook_login_url(client_id)

    return login_url

if __name__ == '__main__':
    app.run(debug=True)

