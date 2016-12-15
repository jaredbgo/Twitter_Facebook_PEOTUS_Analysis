import requests_oauthlib
import webbrowser
import json
import pickle
import pprint
import requests
import unittest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print ""
print "____This program calculates the opinion a Twitter and Facebook user has about our next president____"
print ""
print ""

#GETTIGN TWITTER DATA USING TEXTBOOK CODE
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# Get these from the Twitter website, by going to
# https://apps.twitter.com/ and creating an "app"
# Don't fill in a callback_url; instead, put in a placeholder for the website
# Visit the Keys and Access Tokens tab for your app and grab the following two values

client_key = None# what Twitter calls Consumer Key -- fill in a string here
client_secret = None # What Twitter calls Consumer Secret -- fill in a string here

if not client_secret or not client_key:
    print "You need to fill in client_key and client_secret. See comments in the code around line 8-14"
    exit()

def get_tokens():
    ## Step 1: Obtain a request token which will identify you (the client) in the next step.
    # At this stage you will only need your client key and secret

    # OAuth1Session is a class defined in the requests_oauthlib module
    # Two values are passed to the __init__ method of OAuth1Session
    # -- the key is passed as the value of the first parameter (whose name we don't know)
    # -- the secret is passed as the value of the parameter that is also called client_secret
    # after this line executes, oauth will now be an instance of the class OAuth1Session
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)

    request_token_url = 'https://api.twitter.com/oauth/request_token'

    # invoke the fetch_request_token method of the class OAuth1Session on our instance
    # it returns a dictionary that might look like this:
    # {
    #     "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #     "oauth_token_secret": "Kd75W4OQfb2oJTV0vzGzeXftVAwgMnEK9MumzYcM"
    # }
    # It also saves the oauth_token as an instance variable of the object
    # oauth is bound to, so it can be used in later steps
    fetch_response = oauth.fetch_request_token(request_token_url)

    # pull the two values out of the dictionary and store them in a variable for later use
    # note that d.get('somekey') is another way of writing d['somekey']
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    ## Step 2. Obtain authorization from the user (resource owner) to access their protected resources (images, tweets, etc.). This is commonly done by redirecting the user to a specific url to which you add the request token as a query parameter. Note that not all services will give you a verifier even if they should. Also the oauth_token given here will be the same as the one in the previous step.

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    # append the query parameters need to make it a full url.
    # they will include the resource_owner_key from the previus step,
    # which was stored in the oauth object above as an instance variable
    # when fetch_request_token was invoked
    authorization_url = oauth.authorization_url(base_authorization_url)

    webbrowser.open(authorization_url)

    # After the user authenticates at Twitter, it would normally "redirect"
    # the browser back to our website. But we aren't running a website.
    # Some services, like Twitter, will let you configure the app to
    # display a verifier, or the entire redirect url, rather than actually
    # redirecting to it.
    # User will have to cut and paste the verifier or the whole redirect url

    # version where the website provides a verifier
    verifier = raw_input('Please input the verifier>>> ')

    # version where the website provides the entire redirect url
    # redirect_response = raw_input('Paste the full redirect URL here: ')
    # oauth_response = oauth.parse_authorization_response(redirect_response)
    # get back something like this
    #{
    #    "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #    "oauth_verifier": "sdflk3450FASDLJasd2349dfs"
    #}
    # verifier = oauth_response.get('oauth_verifier')

    ## Step 3. Obtain an access token from the OAuth provider. Save this token so it can be re-used later.
    # In this step we re-use most of the credentials obtained up to this point.

    # make a new instance of OAuth1Session, with several more parameters filled in
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    # get back something like this
    #{
    #    "oauth_token": "6253282-eWudHldSbIaelX7swmsiHImEL4KiNdrY",
    #    "oauth_token_secret": "2EEfA6BG3ly3sR3RjE0IBSnKmrkVU"
    #}
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

try:
    # See if you can read the credentials from the file
    # (If you have credentials for the wrong user, or expired credentials
    # just delete the file creds.txt
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
    # If not, you'll have to get them
    # and then save them in creds.txt
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens

## Step 4. Access protected resources.

# For endpoints that might be interesting to try, see
# https://dev.twitter.com/rest/tools/console and
# https://dev.twitter.com/rest/public
protected_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)

# Call the get method. The work of encoding the client_secret
# and "signing" the request is taken care of behind the scenes.
# The results are also processed for you, including calling .read() and
# encoding as json.
#r = oauth.get(protected_url)
# r is now an instance of the Response class in the requests module
# documentation at
# http://docs.python-requests.org/en/latest/user/quickstart/#response-content

# Of particular interest to us is the json() method of the Response class
#print pretty(r.json())
#raw_input("Enter twitter the screen name you wish to analyze: ")
twitter_screen_name = "FoxNews"
# tweets_count = raw_input("Enter how many tweets you want: ")
tweets_count = 200
params_dic = {"screen_name": twitter_screen_name, "count": tweets_count}

#CACHING CODE MODIFIED FROM TEXTBOOK will take data from API if not already cached, or will take from cached data
cache_fname = "twitter_cached_results.txt"
try:
    fobj = open(cache_fname, 'r')
    saved_cache = pickle.load(fobj)
    fobj.close()
except:
    saved_cache = {}

def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url

def get_with_caching(base_url, params_diction, cache_diction, cache_fname):
    full_url = requestURL(base_url, params_diction)
    # step 1
    if full_url in cache_diction:
        # step 2
        print "retrieving cached result for " + full_url
        return cache_diction[full_url]
    else:
        # step 3
        response = oauth.get(base_url, params=params_diction)
        print "adding cached result for " + full_url
        # add to the cache and save it permanently
        cache_diction[full_url] = response.text
        fobj = open(cache_fname, "w")
        pickle.dump(cache_diction, fobj)
        fobj.close()
        return response.text
#RETRIEVING API OR CACHED DATA, AND ASSIGNING IT TO A VARIABLE
result_text = get_with_caching(protected_url, params_dic, saved_cache, cache_fname)
json_tweets = json.loads(result_text) #this turns results into json
#pprint.pprint(json_tweets)


#r = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json", params = params_dic) # request to the Tweet search endpoint, searching for the phrase 'University of Michigan', looking to get 3 Tweets back

# investigate the data
# print type(r.json())
# print json.dumps(r.json(), indent=2)
# return_data = r.json()
# pprint.pprint(return_data)
# print res.keys()
# # print pretty(res)
# # cache data
# f = open('nested.txt', 'w')
# f.write(json.dumps(res))
# f.close()

#this is creating sentiment lists
pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))
    # creating a class for each twitter post
class Tweet(): #class for each twitter dictionary
    def __init__(self, post_dic = {}): #initializing message, tweeter, and time of each tweet
        if "text" in post_dic:
            self.message = post_dic["text"]
        self.user = post_dic["user"]["screen_name"]
        self.timeposted = post_dic["created_at"]
    def PE_tweet(self):
        # if "donald" or "trump" or "republican" or "gop" or "president elect" or "peotus" in self.message.lower():
        # this medthod checks if the president elect is mentioned in the tweet
        if "trump" in self.message.lower():
            return True
        elif "donald" in self.message.lower():
            return True
        elif "president elect" in self.message.lower():
            return True
        elif "peotus" in self.message.lower():
            return True
        elif "president-elect" in self.message.lower():
            return True
        else:
            return False

    def positive(self): #calculates how many positive sentiment words are in the tweet
        x = 0
        for each in self.message.split():
            if each in pos_ws:
                x += 1
        return x
    def negative(self): #calculates negative sentiment score
        y = 0
        for each in self.message.split():
            if each in neg_ws:
                y += 1
        return y
    def lean(self):
        # a positive lean is that the tweet likes trump, a negative is against him
        if self.PE_tweet() == True: #if the tweet is about trump then caculcate a score
            lean = self.positive() - self.negative()
            return lean
        else:
            return "This tweet is not about the President Elect"


y = Tweet(json_tweets[0]) #this creates a usable instance for test cases

#creates a list of tweet instances for this user
def instance_list(tweet_list):
    tweet_instance_list = []
    for each in tweet_list:
        tweet_instance_list.append(Tweet(each))
    return tweet_instance_list
tweet_instance_list = instance_list(json_tweets)
# def lean_dic(instance_list):
#     lean_dic = {}
#     for each in instance_list
# print pos_ws
# for each in tweet_instance_list:
#     print each.lean()

#this function takes the list of tweets, sees if each tweet is about the president elect. IF IT is about the president elece, it adds to the dicitonary the time of the tweet and the lean score.
def leaning_dict(tweet_list):
    leaning_dict = {}
    for tweet in instance_list(tweet_list): #takes each tweet form list, makes it an instance of Tweet class, then checks if its a trump tweet
        if tweet.PE_tweet() == True: #if it is a trump tweeet
            leaning_dict[(tweet.message, tweet.timeposted)] = tweet.lean() # add it to a dictionary with when it was posted, and value is how biased it is
    return leaning_dict
twitter_lean_dict = leaning_dict(json_tweets) #dictionary of all trump posts and when they were made, and value is lean score

#SORT THE DICIONARY for most biased posts

sorted_twitter_leaning_dict = sorted(twitter_lean_dict, key = lambda x: twitter_lean_dict[x], reverse = True)


overall_tweet_lean = 0 #this next few lines look at all the posts and weighs positive trump tweets vs negative trump tweets"
for each in twitter_lean_dict.keys(): #for each trump post 
    if twitter_lean_dict[each] > 0:#if it looked positively about him, the overall lean went more positive.
        overall_tweet_lean += 1
    elif twitter_lean_dict[each] <0: # If senitment was negative, the accumulator goes down one. 
        overall_tweet_lean = overall_tweet_lean - 1
    else:
        overall_tweet_lean = overall_tweet_lean
def supportive(leanscore): #sees whether more tweets were positive or negative, then prints response
    if leanscore > 0:
        return "Overall, the tweets indicate a FAVORABLE view of our next president!"
    elif leanscore < 0:
        return "Overall, the tweets indicate an UNFAVORABLE view of our next president!"
    elif leanscore == 0:
        return "Overall, the tweets indicate a NEUTRAL view of our next president!"



#LETS GET SOME FACEBOOK DATA
access_token = raw_input("Please enter an access token!\n Check out developers.facebook.com/tools/explorer if unknown: ")
facebook_user_ID = 346937065399354 #raw_input("Please enter the Facebook user ID that you want to analyze here!\n Check out http://findmyfbid.com/ if unknown: ")
####The following code allows us to grade your code with graders' tokens. (It also helps you run the code if your access token has expired.) Please do not change it! 

# print r.status_code
# if r.status_code != 200:
#     access_token = raw_input("Get a Facebook access token v2.3 from https://developers.facebook.com/tools/explorer and enter it here if the one saved in the file doesn't work anymore.  :\n")
# facebook_user_ID = raw_input("Paste the Facebook user ID that you want to analyze here! Check out http://findmyfbid.com/ if unknown: ")


FB_url = "https://graph.facebook.com/v2.3/{}/posts".format(facebook_user_ID)


url_params = {}
url_params["access_token"] = access_token
url_params["fields"] = "message,created_time,from" # Parameter key-value so you can get post message, comments, likes, etc. as described in assignment instructions.
url_params["limit"] = 200 #analyzing data from last 200 tweets

# raw_FB_data = requests.get(FB_url, url_params)

    
# json_FB_data = json.loads(raw_FB_data.text)
# pprint.pprint(json_FB_data)


cache_fname1 = "facebook_cached_results.txt"
try:
    fobj1 = open(cache_fname1, 'r')
    saved_cache1 = pickle.load(fobj1)
    fobj1.close()
except:
    saved_cache1 = {}

raw_FB_data = get_with_caching(FB_url, url_params, saved_cache1, cache_fname1) #collecting facebook data
json_FB_data = json.loads(raw_FB_data) #turning facebook data into json format
# print json_FB_data
# pprint.pprint(json_FB_data)
FB_json_list = json_FB_data["data"] #now data is a list of dictionaries, each is one post

class Post():
    def __init__(self, post_dict={}):
        if 'message' in post_dict:
            self.message = post_dict['message'] #extracts the message of each post
        else:
            self.message = ""
        self.user = post_dict["from"]["name"] #who posted it?
        self.timeposted = post_dict["created_time"] #when was it created? 
    def PE_post(self): #tests if the post is about our next president
        # if "donald" or "trump" or "republican" or "gop" or "president elect" or "peotus" in self.message.lower():
        if "trump" in self.message.lower():
            return True
        elif "donald" in self.message.lower():
            return True
        elif "president elect" in self.message.lower():
            return True
        elif "peotus" in self.message.lower():
            return True
        elif "president-elect" in self.message.lower():
            return True
        else:
            return False

        
    def positive(self): #sees how many positive words were in the post message
        x = 0
        for each in self.message.split():
            if each in pos_ws:
                x += 1
        return x
                   
    def negative(self):
        y = 0
        for each in self.message.split():
            if each in neg_ws:
                y += 1
        return y

    def lean(self):
        # a positive lean is that the post likes trump, a negative is against him
        if self.PE_post() == True: #if the tweet is about trump then caculcate a score
            lean = self.positive() - self.negative() #for each trump tweet, it is possitive or negative?
            return lean
        else:
            return "This post is not about the President Elect"

facebook_instance_list = [] #this is creating a list of post instances
for each in FB_json_list: #turning each dictionary into a post instance
    facebook_instance_list.append(Post(each)) # creating list of instances

facebook_leaning_dict = {} #for each post, if its a trump post, it adds it to a dictionary, which keeps its message and time posted and how biases it was
for post in facebook_instance_list:
    if post.PE_post() == True:
        facebook_leaning_dict[(post.message, post.timeposted)] = post.lean()
# print facebook_leaning_dict

#SORT THE DICIONARY for most biased posts

sorted_facebook_leaning_dict = sorted(facebook_leaning_dict, key = lambda x: facebook_leaning_dict[x], reverse = True)

overall_post_lean = 0 #this code sees how many posts are positive, how many are negative, and aggregates a score
for each in facebook_leaning_dict.keys():
    if facebook_leaning_dict[each] > 0:
        overall_post_lean += 1
    elif facebook_leaning_dict[each] < 0:
        overall_post_lean = overall_post_lean - 1
    else:
        overall_post_lean = overall_post_lean
def supportive1(leanscore): #If 
    if leanscore > 0:
        return "Overall, the posts indicate a FAVORABLE view of our next president!"
    elif leanscore < 0:
        return "Overall, the posts indicate an UNFAVORABLE view of our next president!"
    elif leanscore == 0:
        return "Overall, the posts indicate a NEUTRAL view of our next president!"

print "__________________________________________________________"
print "***** TWITTER RESULTS FOR USER {}{} *****".format("@", twitter_screen_name)
print "__________________________________________________________"
print ""
# print json_FB_data["data"][0]["from"]["name"]
print "The top 3 most supportive tweets:"
print ""
for each in sorted_twitter_leaning_dict[:3]:
    print str(each[0]) 
    print "This post was created at this time: " + str(each[1])
    print ""
print supportive(overall_tweet_lean) 
print ""
print "__________________________________________________________"

print "***** FACEBOOK RESULTS FOR USER " + json_FB_data["data"][0]["from"]["name"] +  " *****"
print "__________________________________________________________"
print ""

print "The top 3 most supportive Facebook posts:"
print ""
for each in sorted_facebook_leaning_dict[:3]:
    print str(each[0])
    print "This post was created at this time: " + str(each[1])
# .format(str(sorted_facebook_leaning_dict[:5]), reverse = True)
    print ""
print supportive1(overall_post_lean) 

# class Hi(unittest.TestCase):

#     def test_json(self):
#         xy = json_tweets
#         self.assertEqual(type(xy), type("hi") #testing that json_tweets returns a string
#     # def test_presidential_tweet(self):
#     #     self.assertTrue(Tweet({"text": "Trump is great"}).PE_tweet() == True) #testing that PE_tweet is working correctly
#     # def test_tweet_message(self):
#     #     self.assertEqual(type(y.message), type("message")) #this is testing that Tweet class, message instance was created correctly
#     # def test_supportive_test(self):
#     #     self.assertEqual(supportive(0),"Overall, the tweets indicate a NEUTRAL view of our next president!") #testing that supprtive is working correctly
#     # def test_FB_instance(self):
#     #     self.assertEqual(type(facebook_instance_list[0].PE_post()),type(False)) #testing that PE_tweet is giving correct output type
#     # def test_6(self):
#     #     self.assertTrue("true" == "true")
# unittest.main(verbosity=2)
print ""
print ""
print ""
print "___ TEST CASES ___"
class AllMyTests(unittest.TestCase):
    def test_json(self):
        self.assertEqual(type(json_tweets), type([]))
    def test_presidential_tweet(self):
        self.assertTrue(Tweet({"text": "Trump is great", "user":{"screen_name":"hi"}, "created_at": "51"}).PE_tweet() == True)
    def test_tweet_message(self):
        self.assertEqual(type(y.message), type(u"message"))
    def test_supportive(self):
        self.assertEqual(supportive(0), "Overall, the tweets indicate a NEUTRAL view of our next president!")
    def test_FB_instance(self):
        self.assertEqual(type(facebook_instance_list[0].PE_post()), type(False))
    def test_json_length(self):
        self.assertEqual(len(facebook_instance_list), 200)
unittest.main(verbosity = 2)







