from frappe import *
from frappe.utils import get_url, cint
import requests
import urllib.parse


# Function to get the Facebook login URL
def get_facebook_login_url(RHA_id):
    """
    Input :   RHA_id: The ID of the Facebook app.
    Output:   Returns the URL for Facebook login.
    """
    # Initialize the parameters
    params = {
        "client_id": RHA_id,
        "redirect_uri": get_url('facebook-callback'),
        "scope": "user_photos, publish_to_groups",
        "response_type": "code"
    }

    # Generating the facebook login url
    login_url = "https://www.facebook.com/v12.0/dialog/oauth?" + urllib.parse.urlencode(params)

    return login_url


# Function to exchange the authorization code for an access token
def exchange_code_for_access_token(code, RHA_id, RHA_app_secret):
    """
    Input:   code: The authorization code returned by Facebook.
             RHA_id: The ID of the Facebook app.
             RHA_app_secret: The secret key of the Facebook app.
    Output:  The access token returned by Facebook.
    """

    token_params = {
        "client_id": RHA_id,
        "client_secret": RHA_app_secret,
        "redirect_uri": get_url('facebook-callback'),
        "code": code
    }

    response = requests.get("https://graph.facebook.com/v12.0/oauth/access_token", params=token_params)

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
    RHA_id = '<facebook_app_id>'
    RHA_app_secret = '<facebook_app_secret>'
    photo_url ='https://cdn.pixabay.com/photo/2013/07/18/10/56/railroad-163518_960_720.jpg'

    # The authorization code returned by Facebook
    code = frappe.form_dict.get('code')

    # Exchange the authorization code for an access token
    access_token = exchange_code_for_access_token(code, RHA_id, RHA_app_secret)

    # Share the photo on Facebook using the access token
    share_response = share_photo_on_facebook(access_token, photo_url)

    if share_response.get('error'):
        frappe.throw(_("Error sharing photo on Facebook"))
    else:
        frappe.msgprint(_("Photo shared successfully on Facebook"))

        
        
# Define a new route to generate the Facebook login URL
@frappe.whitelist(allow_guest=True)
def get_facebook_login_url_route():
    """
    Route for generating the Facebook login URL.
    """
    RHA_id = 'facebook_app_id'
    login_url = get_facebook_login_url(RHA_id)

    return login_url
  

    
# Define a new route to handle the Facebook callback
@frappe.whitelist(allow_guest=True)
def facebook_callback_route():
    """
    Route for handling the Facebook callback.
    """
    facebook_callback()


