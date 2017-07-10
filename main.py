import requests, colorama
import urllib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from termcolor import *
from textblob.sentiments import NaiveBayesAnalyzer
from apptocken import APP_ACCESS_TOKEN
BASE_URL = 'https://api.instagram.com/v1/'
colorama.init()

#self
#insta id = akashdeep_gill_

def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'User does not exist!'
  else:
    print 'Status code other than 200 received!'


#to get user id
#user_id= vivek_shivam

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()






#getting info of other user
#user_id= vivek_shivam

def get_user_info(insta_user):
    user_id = get_user_id("vivek_shivam")
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received'











#post
#here post is set to [0] which means taking recent post



def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            n_th_post = int(raw_input("which post"))
            image_name = own_media['data'][n_th_post]['id'] + '.jpeg'
            image_url = own_media['data'][n_th_post]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'






#user post
#here post is set to [0] which means taking recent post of user
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            n_th_post = int(raw_input("which post"))
            image_name = user_media['data'][n_th_post]['id'] + '.jpeg'
            image_url = user_media['data'][n_th_post]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



# list of people who have liked the post of user



def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    users_info = requests.get(request_url).json()
    i = 0
    if users_info['meta']['code'] == 200:
        if len(users_info['data']):
            for ele in users_info['data']:
                print (users_info['data'][i]['username'])
                i = i + 1
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
    exit()




#liking post
#user_id= vivek_shivam


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()




def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'




# getting list of comments on user post

def comment_info(insta_username):
    get_user_id(insta_username)


    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info1 = requests.get(request_url).json()
    if comment_info1['meta']['code'] == 200:
        if len(comment_info1):
            a=0
            while a<len(comment_info1)-1:
                print "%s commented : %s"%(comment_info1["data"][a]["from"]["username"],comment_info1["data"][a]["text"])
                a=a+1
        else:
            print "no data"
    else:
        print"code not 200"


#commenting on a post


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("comment here: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"





# deleting negative comment


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()


                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'




#hash tags

def trend_id():
    hash_dict = {}
    tag = raw_input("enter trend : ")
    request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') % (tag, APP_ACCESS_TOKEN)
    media_tag = requests.get(request_url).json()

    if media_tag['meta']['code'] == 200:

        if media_tag['data']:

            for x in range(0, len(media_tag['data'])):
                tags = media_tag['data'][x]['tags']
                print tags


                for y in range(0, len(tags)):

                    if media_tag['data'][x]['tags'][y] in hash_dict:
                        hash_dict[media_tag['data'][x]['tags'][y]] += 1

                    else:
                        hash_dict[media_tag['data'][x]['tags'][y]] = 1

                print hash_dict

        else:
            print'post not exist'

    else:
        print 'ERROR'
    hash_dict.pop(tag.lower(), None)
    print hash_dict
    wordcloud = WordCloud().generate_from_frequencies(hash_dict)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()

    # downloading recent media liked by user

def recent_media_liked():
        request_url = BASE_URL + "users/self/media/liked?access_token=%s" % (APP_ACCESS_TOKEN)
        recently_liked_media = requests.get(request_url).json()

        if recently_liked_media["meta"]["code"] == 200:
            if len(recently_liked_media["data"]):
                image_name = recently_liked_media["data"][0]["id"] + ".jpeg"
                image_url = recently_liked_media["data"][0]["images"]["standard_resolution"]["url"]
                urllib.urlretrieve(image_url, image_name)
                print "Your image has been downloaded!"
            else:
                print "User does not exist!"
        else:
            print "Status code other than 200 received!"

        # function download posts with atleast some specific minimum number of likes
def download_post_by_likes():
    request_url = BASE_URL + "users/self/media/recent/?access_token=%s" % (APP_ACCESS_TOKEN)
    own_media = requests.get(request_url).json()
    x = 0
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            like_count = int(raw_input("Enter the minimum likes for a post(in numeric)"))
            for x in range(0, len(own_media["data"])):
                if own_media["data"][x]["likes"]["count"] > like_count:
                    image_name = own_media['data'][x]['id'] + '.jpeg'
                    image_url = own_media['data'][x]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    print 'Your image has been downloaded!'
                    x = x + 1
                else:
                    x = x + 1
                    print str(x) + "th picture cannot be downloaded as likes are less"

        else:
                print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


#startbot asking user to enter input



def start_bot():
    while True:
        print '\n'
        cprint ('Hey! Welcome to instaBot!',"blue")
        cprint ('Here are your menu options:\n',"blue")
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.enter to know sub trendding\n"
        print "k.Recent media liked by user"
        print "l.Download the post which have certain minimum number of likes"
        cprint ('m.Exit',"red")

        choice = raw_input("Enter your choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Username not valid in instagram!!!', "red")
            else:
                get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Username not valid in instagram!!!', "red")
            else:
                get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
               cprint('Username not valid in instagram!!!', "red")
           else:
               get_like_list(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
               cprint('Username not valid in instagram!!!', "red")
           else:
               like_a_post(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
               cprint('Username not valid in instagram!!!', "red")
           else:
               comment_info(insta_username)
        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
               cprint('Username not valid in instagram!!!', "red")
           else:
               post_a_comment(insta_username)
        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
               cprint('Username not valid in instagram!!!', "red")
           else:
               delete_negative_comment(insta_username)
        elif choice=="j":
            trend_id()
        elif choice=="k":
            recent_media_liked()
        elif choice=="l":
            download_post_by_likes()

        elif choice == "m":
            exit()
        else:
            print "wrong choice"

start_bot()

