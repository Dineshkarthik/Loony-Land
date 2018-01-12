"""Script to get user uid."""
from fbchat import Client
from fbchat.models import *

client = Client('<email>', '<password>')
user = client.searchForUsers('<name of user>')[0]

print('user ID: {}'.format(user.uid))
print("user's name: {}".format(user.name))
print("user's photo: {}".format(user.photo))
print("Is user client's friend: {}".format(user.is_friend))
