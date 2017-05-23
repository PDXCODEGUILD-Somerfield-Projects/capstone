# genius loci
PDX Code Guild capstone project

## Summary
Using a browser's latitude and longitude coordinates, the application pulls local tweets from Twitter and creates a bubble visualization 
of the most frequent words, hashtags, and user mentions.

## Description
The project is set up using the Django web framework. Latitude and Longitude are pulled using Geolocation. Three-legged-Oauth 1.0 
is used to authenticate the user so that streaming data may be used (in the near future). The Twitter Search API is used to query tweets 
within a 5 mile radius. Deserialization and data processing is done in Python and the results are displayed using 
D3.js bubble chart. The user's query history is saved so that any query may be viewed again.


## Using the app
The user is automatically directed to Twitter for authorization. Once they give permission they are redirected back to the home page. 
To use the app, the user simply clicks the 'Start Locating' button. (User permission is also needed in order to fetch location coordinates.) 
After a moment of processing, a bubble chart will display the most frequent local words, hashtags, and user mentions. Circle size and 
depth of color is determined by the frequency of the word or hashtag in the local tweets.

The 'Query History' tab allows the user to view a list of their queries. 'Run Search' will redisplay that query's search results.
Users may also delete queries they no longer wish to keep.

Please note that while the app filters out the most common English words (such as 'the', 'and', 'a'), it does not filter words that some
users may consider profane.

![Alt text](https://cloud.githubusercontent.com/assets/25858061/26338237/4a3a6c18-3f33-11e7-9a0a-f7ccdbbd4a03.jpg "Bubble Chart")

## Setup
Requirements: 
Registered Twitter app (needed to set up the redirect url and to get a Twitter Consumer Key and Secret, 
Django, Python 3.6, oauthlib
