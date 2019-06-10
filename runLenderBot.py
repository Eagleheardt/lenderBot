import decode as de
import lendingLibraryAdapter as adapter

import sqlite3
from sqlite3 import Error
import time
import datetime
import random
import os

from datetime import datetime
from slackclient import SlackClient

###############################
###   Get the slack token   ###
###############################

de.MAIN_KEY = "data/lenderBot"
# de.MAIN_KEY = "lenderBot/data/lenderBot" # prod location
slack_client = SlackClient(de.getToken())

###############################
###   End the slack token   ###
###############################

############################################################################
############################################################################

# lenderBot's user ID in Slack: value is assigned after the bot starts up
templateID = None

# CONSTANTS
RTM_READ_DELAY = 0.5 # 0.5 second delay in reading events

###########################
###   Snarky Comments   ###
###########################

notAdmin = "Only the powerful can use this command!"
notDirect = "That is a DM only command, weakling!"
what = "I don't understand."
what2 = "I have no idea what you mean."
what3 = "That makes no sense!"
what4 = "I have half a mind to send you to the Avatar of Mitra!"
notEnough = "I can't add that, imbecile!"

notFound = "I couldn't find that! Perhaps it fell off a cliff."
notFound2 = "Despite my best efforts, that has been lost to time."

conanTells = "Listen well and I shall tell you of who I am!"
aboutConan = "<https://www.youtube.com/watch?v=mZHoHaAYHq8|Conan the Librarian>"

############################################################################
############################################################################

###################################
###   Slack Response commands   ###
###################################

def parseSlackInput(aText):
	if aText and len(aText) > 0:
		item = aText[0] # gets first (only) item
		if 'text' in item:
			msg = item['text'].strip(' ') # text of the message
			chn = item['channel'] # ID of the channel
			usr = item['user'] # ID of the user
			stp = item['ts'] # Timestamp at which message was posted
			return [str(msg),str(chn),str(usr),str(stp)]
		else:
			return [None,None,None,None]

def inChannelResponse(channel,response):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response,
		as_user=True
		)
	return

def threadedResponse(channel,response,stamp):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response,
		thread_ts=stamp,
		as_user=True
		)
	return

def directResponse(someUser,text):
	slack_client.api_call(
		"chat.postMessage",
		channel=someUser,
		text=text,
		as_user=True
		)
	return

############################
###   Parsing commands   ###
############################

def parseMedia_insert(mediaInfo):
	try:
		result = [x.strip() for x in mediaInfo.split(',', 4)]
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMedia_select(mediaInfo):
	try:
		result = [x.strip() for x in mediaInfo.split(',', 4)]
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMediaType_select(mediaInfo):
	try:
		result = [x.strip() for x in mediaInfo.split(',', 4)]
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMediaCategory_select(mediaInfo):
	try:
		result = [x.strip() for x in mediaInfo.split(',', 4)]
	except: # if there aren't enough parts
		return False # returns false
	return result

##################################################################################################################################

def handle_command(command, channel, aUser, tStamp):
	
	command = command.lower()
	response = None
    
	if command == "!test":
		response = (("""Text:{0}
				Channel:{1}
				TS:{2}
				User:{3}
				""").format(command,channel,tStamp,aUser))
		inChannelResponse(channel,response)
		return
	    
	if command == "!fact":
		# need to generate a random Conan fact
		return

	if command == "!who":
		inChannelResponse(channel, conanTells)
		directResponse(aUser, aboutConan)
		return

	##########################
	###   ADMIN commands   ###
	##########################

	adminDMIDs = {
		'DK9JT0TMJ' : "Andre Gueret",
		'DK1G58Q0K' : "Daniel Hodge",
		'DKCVBJPNC' : "Tony Strickland"
	}

	# if command == "!admin":
	# 	if adapter.isAdmin(aUser):
	# 		inChannelResponse(channel,"I'm an admin!")
	# 		return
	# 	inChannelResponse(channel,"Not an admin.")
	# 	return

	#########################
	###   !addMediaType   ###
	#########################

	if command.startswith("!addMediaType".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
				mediaInfo = command[len("!addMediaType")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaType(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the types of media carried by the backs of our enemies!""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#############################
	###   !addMediaCategory   ###
	#############################

	if command.startswith("!addMediaCategory".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
				mediaInfo = command[len("!addMediaCategory")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaCategory(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the categories of media! This pleases Ymir!""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#############################
	###   !addMediaCategory   ###
	#############################

	if command == "!allMediaCategory".lower():
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaCategory(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the categories of media! This pleases Ymir!""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#############################
	###   !getMediaCategory   ###
	#############################

	if command.startswith("!getMediaCategory".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
				mediaInfo = command[len("!getMediaCategory")+1:].strip()
				if len(mediaInfo) >= 3 and len(mediaInfo) < 20:
					sqlResult = adapter.get_MediaCategoryID(mediaInfo)
					if sqlResult != -1:
						inChannelResponse(channel,"I see {}".format(sqlResult)) # success
						return
					else:
						inChannelResponse(channel, notFound2)
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what3)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#####################
	###   !addMedia   ###
	#####################

	if command.startswith("!addMedia".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
				mediaInfo = command[len("!addMedia")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_Media(mediaInfo)
					# need to parse out and insert data later
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the hoard!""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	######
	return 

	##############################
	###   End handle_command   ###
	##############################

##################################################################################################################################

if __name__ == "__main__":
	if slack_client.rtm_connect(with_team_state=False):
		print("Lenderbot is running!")
		# Read bot's user ID by calling Web API method `auth.test`
		templateID = slack_client.api_call("auth.test")["user_id"]
		while True:
			try:
				command, channel,usr,stp = parseSlackInput(slack_client.rtm_read())
				if command:
					handle_command(command, channel,usr,stp)
			except:
				pass
                
		time.sleep(RTM_READ_DELAY)
	else:
		print("Connection failed. Exception traceback printed above.")