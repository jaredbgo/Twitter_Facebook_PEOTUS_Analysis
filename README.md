# Twitter_Facebook_PEOTUS_Analysis
Program to analyze Twitter and Facebook profile opinions towards the President Elect
Tweet Post Analysis by Jared Goldberg


This program takes a twitter account and a Facebook account, and analyzes 200 of the most recent posts from each to determine whether or not the account holds a favorable view of President Elect Donald Trump. The output prints 3 of the most supportive tweets and posts, and then a statement for each account about whether the user generally supports Mr. Trump. 

To run my program, you must get a Consumer Key and Secret from Twitter. Do do this, use your twitter account to create an app at https://dev.twitter.com/rest/public. Click “My apps” at the top right of the page. Then, create an app, and assign the variable client_key (line 25) to a string of the Consumer Key (API Key) that you recieved. Then, assign the variable client_secret (line 26) to a string of the Consumer Secret (API Secret) that you received. 

Now, you should have the Tweet_Post_Analysis.py, twitter_cached_results.txt, facebook_cached_results.txt, negative-words.txt, and positive-words.txt in the same directory. 
In the python file, you can choose which profiles to analyze by assigning twitter_screen_name (line 152) to a string of a twitter username, and /or assigning facebook_user_ID (line 321) to the ID of a Facebook account (http://findmyfbid.in/ can be useful).

Then, in your command window go to the directory with these files. You are ready to run the python file! Run it, and a web page will pop up asking if the program can access your account. Allow this access, then paste the PIN that is displayed on the web page into your command window where it says “Please input the verifier>>>”. Press return/enter. 

Then, the program will ask you to enter a Facebook access token. Get this from https://developers.facebook.com/tools/explorer/, and make sure that user_status, user_posts, and user_managed_groups are all checked! Paste this in the command window, and press return/enter. 

Then the program should execute fully, and it will print out top tweets and posts, when they were posted, and a sentence about overall favorability towards President Elect Trump.

Tweet_Post_Analysis.py — all of the program code. 
twitter_cached_results.txt — file with cached data from Twitter.
facebook_cached_results.txt — file with cached data from Facebook. 
negative-words.txt — list of positive sentiment words
positive-words.txt — list of negative sentiment words


REFERENCES

http://stackoverflow.com/questions/31137552/unicodeencodeerror-ascii-codec-cant-encode-character-at-special-name — used this website because I was having an error printing unicode strings

http://ptrckprry.com/course/ssd/data/positive-words.txt — positive sentiment text file
http://ptrckprry.com/course/ssd/data/negative-words.txt — negative sentiment text file
