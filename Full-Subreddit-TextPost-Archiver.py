#! /usr/bin/python3
import praw, os, sys, datetime, time
start = time.time()

#if usedarkmode:
textcolor = "e2e2e2"
postbg = "333"
bgcolor = "212121"
shadow = "000"
link = "add8e6"
hoverlink = "fff"
visitedlink = "adbce6"
#else:
#	textcolor = "000"
#	postbg = "e6e6e6"
#	bgcolor = "fff"
#	shadow = "636363"
#	link = "386fff"
#	hoverlink = "759bff"
#	visitedlink = "ba75ff"

# Setting Variables
client_id = " "
client_secret = " "
subname = sys.argv[1]
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='Text Post Archiver')
postnumber = 0

if client_id == " " or client_secret == " ":
	print("You need to put a client id and client secret into the script!")
	sys.exit()

# Making directory with the title of the selected subreddit
os.makedirs(subname, exist_ok=True)

# Gets a post's submission date and time
def getdate(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)

# Makes a blank html file and writes data to it
postslist = open(subname+' Post Archive.html', "a")
archive = """<html>
<LINK REL=StyleSheet HREF=\""""+subname+'/'"""style.css" TYPE="text/css">
<center><head>Posts from /r/"""+subname+"""</head></center>
<body> <br> <br>\n"""
postslist.write(archive)

# Making lists for the posts' data to go into
global scores
scores = []
global postlist
postlist = []

# Function for downloading and writing posts and comments
def dothestuff():

	# Makes an html file for the current post and sets the file's name to the post's id
	savepost = open(os.path.join(subname, submission.id+'.html'), "a")

	# Increases the index of posts downloaded by 1. Used to display "Saving Post #___..." in console
	global postnumber
	postnumber+= 1
	print('Saving Post #'+str(postnumber)+': '+submission.title)

	# Setting variable to be added to the submission's html file (The ".replace"s fix some errors that make the browser unable to read certain characters properly)
	if submission.selftext_html is not None:
		post = """<html>
<link rel=StyleSheet href="style.css" type="text/css">
<head></head>
<body> \n<p>"""+submission.title.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p> <div class="mainpost"> <p>"""+submission.selftext_html.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p> </div>"""
	else:
		post = """<html>
<link rel=StyleSheet href="style.css" type="text/css">
<head></head>
<body> \n<p>"""+submission.title.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p>"""
	
	# Writing current post's title and content to its html file
	savepost.write(post)

	# Closes the html tags for the current submission's file
	finish = """ </body> </html>"""
	savepost.write(finish)
	savepost.close()

	# Gets the post's author, score, number of comments, date, and title to be added to the main html file, then adds them
	currentpost = """ <div class="postinfo"> """+str(submission.author)+' ['+str(submission.score)+' points] '+'['+str(submission.num_comments)+' comments] '+str(getdate(submission))+' '+""" <br> <a href=\""""+subname+'/'+submission.id+'.html'+'">'+submission.title.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+'</a> </div> <br>\n\n'""""""
	scores.append(submission.score)
	postlist.append(currentpost)

# Gets and downloads submissions and comments, then adds them to the "Archive" html file in the current directory
for submission in reddit.subreddit(subname).submissions():
	dothestuff()

# Sorting the posts by score, then writing them to the list file
postlist_sorted = [postlist for scores, postlist in sorted(zip(scores, postlist), reverse=True)]
global postindex
postindex = 0
for thing in postlist_sorted:
	postindex += 1
	postslist.write('#'+str(postindex)+'\n'+thing+'\n\n\n\n')

# Closes the Main html file's tags
finished = """</body> </html>"""
postslist.write(finished)
postslist.close()

# Writing a "style.css" file to be used by the downloaded html files
cssfile = open(os.path.join(subname, 'style.css'), "a")
csscode = """.acomment{
	color: #"""+textcolor+""";
	background-color: #"""+postbg+""";
	padding-left: 10px;
	width: 1000px;
	padding-right: 10px;
	min-height: 10em;
	display: table-cell;
	vertical-align: middle;
	box-shadow: 5px 5px 10px #"""+shadow+""";
	}

.bcomment{
	color: #"""+textcolor+""";
	background-color: #"""+postbg+""";
	padding-left: 10px;
	padding-top:5px;
	padding-bottom: 5px;
	margin-left: 50px;
	width: 1000px;
	padding-right: 10px;
	box-shadow: 5px 5px 10px #"""+shadow+""";
	}

.bcommentinfo{
	margin-left: 50px;
}

.postinfo{
	color: #"""+textcolor+""";
	margin: auto;
	background-color: #"""+postbg+""";
	padding-left: 10px;
	width: 1000px;
	padding-right: 10px;
	box-shadow: 5px 5px 10px #"""+shadow+""";
	padding-bottom: 10px;
	padding-top: 5px;
}

.mainpost{
	color: #"""+textcolor+""";
	background-color: #"""+postbg+""";
	box-shadow: 5px 5px 10px #"""+shadow+""";
	padding-left: 10px;
	padding-right: 10px;
	padding-bottom: 10px;
	padding-top: 5px;
	display: block;
	margin: auto;
	width: 90%;
}

body{
	background-color: #"""+bgcolor+""";
	color: #"""+textcolor+""";
}

A:link {
	color: #"""+link+""";
	font-weight: bold;
}

A:visited {
	color: #"""+visitedlink+""";
	font-weight: bold;
}

A:hover {
	color: #"""+hoverlink+""";
}
	"""
cssfile.write(csscode)
cssfile.close()
print('Got '+str(postnumber)+' posts in {0:0.1f} seconds'.format(time.time() - start))
