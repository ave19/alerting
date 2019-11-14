#!/usr/bin/env python
# 
# Proof of Concept for Alerting from Pythong
#
# By Dave Jaccard
# david.jaccard@elastic.co
#

from elasticsearch import Elasticsearch, client
import certifi
import smtplib


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Elastic Stack Settings
# username and password for the alert user
auth = ( 'elastic', 'password' )

# index you want to query against, could be a pattern.
target_index = 'the-index-with-the-alert-stuff'

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Email Settings
email_user   = "email_person"
email_pwd    = "email_password"
email_server = smtplib.SMTP('smtp.gmail.com', 587)

#Next, log in to the server
email_server.login(email_user, email_pwd)

#
# How to do the certificate thing:
#   0.  `pip install certifi`
#   1.  Find where your python will look for certificates.
#   1.1  Open a terminal and do this:
#
# deltav:alerts ave$ python
# Python 2.7.10 (default, Feb 22 2019, 21:55:15) 
# [GCC 4.2.1 Compatible Apple LLVM 10.0.1 (clang-1001.0.37.14)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import certifi
# >>> print certifi.where()
# /Users/ave/env/alerts/lib/python2.7/site-packages/certifi/cacert.pem
# >>> 
#
#   2.  Use Firefox (or something) to get the root CA for the Elastic cluster
#       you want to go to.  
#   2.1.  Concatenate (cat) the contents of that certificate to the end of the
#         the cacert.pem file.  You might wanna google that first.
#
#  cat that_firefox_cert.pem >> /Users/ave/env/alerts/.../certifi/cacert.pem
#

#
# This object will connect to Elasticsearch whenever you need something.
# https://elasticsearch-py.readthedocs.io/en/master/
e = Elasticsearch(
	"https://your-cluster-here:9243",
	http_auth=auth,
	use_ssl=True,
	verify_certs=True,
	ca_certs=certifi.where(),
	request_timeout=30000
	)

#
# This is a 'client' helper
# https://elasticsearch-py.readthedocs.io/en/master/api.html#indices
indices = client.IndicesClient(e)

print e.info()

#
# Go into the console of Kibana for the cluster you want to pull this alert 
# from.  Work a query over and over until you're satisfied that it will do the
# right thing.  Paste that query in here as the alert_query.  Your goal is to 
# make a query that has a `{ "hits": { "hits": [] } }` so don't 
# do `{ "size": 0 }`

alert_query_body = '''
{ ... }
'''

result = e.search(
  index=target_index, 
  body=alert_query_body
  )

# This could be used to drop certain kinds of things...
# This will not alert if an item in the list appears in the hit
blacklist = [ "thing1", "thing2", "thing3" ]

if len(result['hits']['hits']) > 0:
  for hit in result['hits']['hits']:

	# The 'item' is a string...
	for item in blacklist:
     		# See if the blacklisted item is in the hit...
		if item in hit['location']:
			continue


	# There's hits to process....
	print "Hits detected."
	# Send the mail, you need the new line...
	msg = "
	Hello!" # The /n separates the message from the headers
	server.sendmail("you@gmail.com", "target@example.com", msg)

else:

	print "No hits detected."
	# There are no hits.

