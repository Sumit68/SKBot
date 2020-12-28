import psycopg2
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import logging
import telegram
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
					  ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler,
						  Filters, CallbackQueryHandler, ConversationHandler)
from telegram.utils.helpers import mention_html

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

from database import DBHelper
db = DBHelper()
from sqlitetopdf import CustomPDF
Pdf = CustomPDF()
from sendmail import SendMail
s = SendMail()

FIRST, SECOND, TYPING, DELETING, EXP = range(5)
DIVA, DIVB, DIVC, DIVD, addevent, delevent, listevent, Phy, Chem, CP, ED = range(11)
MAILING, THIRD, FOURTH = range(3)
sendpdf, mailpdf = range(2)



def start(update, context):
	v = update.effective_user.id
	username = update.effective_user.full_name
	print("Hello")
	update.message.reply_text('Hello ' + str(username) + '! Please Select /about to know about our features.Visit us at <a href="http://skbot.epizy.com/"><i>http://skbot.epizy.com/</i></a> for more information.',parse_mode=telegram.ParseMode.HTML)
	db.newUser(v, username)

def about(update, context):
	update.message.reply_text(
				'<i>Here is our entire command list.</i>\n'
				'<i>/attendance</i> = Lets you Mark your attendance.\n'
				'<i>/view</i> = Shows you your attendance Percentage.\n'
				'<i>/experiment</i> = Links to all subject manuals/experiments.\n'
				'<i>/timetable</i> = Sends you Timetable based on your division.\n'
				'<i>/event</i> = Shows ongoing and scheduled events.\n'
				'<i>/pdfview</i> = Provides you with your attendance Report in pdf format.\n',parse_mode=telegram.ParseMode.HTML)


def experiment(update, context):
	keyboard_exp = [[InlineKeyboardButton("Physics", callback_data=str(Phy)),
			   InlineKeyboardButton("Chemistry", callback_data=str(Chem))],
			   [InlineKeyboardButton("CPrograming", callback_data=str(CP)),
			   InlineKeyboardButton("Engineering Drawing", callback_data=str(ED))]]
	reply_markup = InlineKeyboardMarkup(keyboard_exp)
	update.message.reply_text('Select the Subject you want to view experiments for:', reply_markup=reply_markup)
	return EXP

def pdfview(update, context):
	v = update.effective_user.id
	Name = update.effective_user.full_name
	Pdf.chart(v, Name)
	Pdf.simple_table(v, Name)
	keyboard_pdf = [[InlineKeyboardButton("Send document", callback_data=str(sendpdf)),
			   InlineKeyboardButton("Mail Document", callback_data=str(mailpdf))]]
	reply_markup = InlineKeyboardMarkup(keyboard_pdf)	
	update.message.reply_text('How do You Want Your Document.', reply_markup=reply_markup)
	return THIRD	   

def SendDocument(update, context):
	v = update.effective_user.id
	Name = update.effective_user.full_name
	context.bot.send_document(chat_id=update.effective_chat.id,document=open(str(Name)+'.pdf', 'rb'))
	if os.path.exists(str(Name)+'.pdf'):
		os.remove(str(Name)+'.pdf')
	if os.path.exists(str(Name)+'.png'):
		os.remove(str(Name)+'.png')
	return ConversationHandler.END
	
def MailDocument(update, context):
	v = update.effective_user.id
	Name = update.effective_user.full_name
	record = db.newEmail(v)
	if record[0] is None:
		text = 'Please Send us Your Email id.'
		context.bot.send_message(chat_id=update.effective_chat.id,text=text)
		return MAILING
	else:
		record = list(record)
		Email = record[0]
		keyboard_mail = [[InlineKeyboardButton("Yes", callback_data='update'),
			   InlineKeyboardButton("No", callback_data='send')]]
		reply_markup = InlineKeyboardMarkup(keyboard_mail)
		text = 'We are sending you mail at ' + record[0] + ' Do you want to update your email id?'	
		context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=reply_markup)
		return FOURTH
		
def updateemail(update,context):
	v = update.effective_user.id
	Name = update.effective_user.full_name
	text = 'Please Send us Your New Email id.'
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return MAILING

def mailing(update, context):
	v = update.effective_user.id
	Email = update.message.text
	Name = update.effective_user.full_name
	db.updateemail(v,Email)
	s.sendmail(Name, Email)
	text = 'Email has been sent.'
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	if os.path.exists(str(Name)+'.pdf'):
		os.remove(str(Name)+'.pdf')
	if os.path.exists(str(Name)+'.png'):
		os.remove(str(Name)+'.png')
	return ConversationHandler.END


def sendmail(update, context):
	v = update.effective_user.id
	Name = update.effective_user.full_name
	record = db.newEmail(v)
	Email = record[0]
	s.sendmail(Name, Email)
	text = 'Email has been sent.'
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	if os.path.exists(str(Name)+'.pdf'):
		os.remove(str(Name)+'.pdf')
	if os.path.exists(str(Name)+'.png'):
		os.remove(str(Name)+'.png')
	return ConversationHandler.END

def Physics(update, context):
	exp = db.get_item1()
	text = 'These are the Experiments'
	for row in exp:
		text = ((text) + '\n' + str("{0}){1}".format(row[0], row[1]))+'\n')
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return ConversationHandler.END

def Chemistry(update, context):
	exp = db.get_item1()
	text = 'These are the Experiments'
	for row in exp:
		text = ((text) + '\n' + str("{0}){1}".format(row[0], row[2]))+'\n')
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return ConversationHandler.END

def CPrograming(update, context):
	exp = db.get_item1()
	text = 'These are the Experiments'
	for row in exp:
		text = ((text) + '\n' + str("{0}){1}".format(row[0], row[3]))+'\n')
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return ConversationHandler.END

def EngineeringDrawing(update, context):
	exp = db.get_item1()
	text = 'These are the Experiments'
	for row in exp:
		text = ((text) + '\n' + str("{0}){1}".format(row[0], row[4]))+'\n')
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return ConversationHandler.END


def event(update, context):
	keyboard = [[InlineKeyboardButton("Add", callback_data=str(addevent)),
			   InlineKeyboardButton("Delete", callback_data=str(delevent)),
			   InlineKeyboardButton("List", callback_data=str(listevent))]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Select Your Action:', reply_markup=reply_markup)
	return SECOND

def list_event(update, context):
	results = db.get_item()
	text = 'These are the events and their dates'
	for row in results:
		text = ((text) + '\n' + str("{0} {1}".format(row[0], row[1]))+'\n')
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return ConversationHandler.END

def add_event(update, context):

	text = 'To add an event, send me the event details in the following format:\n'\
				  'Name DATE(DD-MM-YYYY)\n'\

	example = 'Hackathon,31-08-2019'

	query = update.callback_query
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	context.bot.send_message(chat_id=update.effective_chat.id,text=example)
	return TYPING

def delete_event(update, context):
	text = 'To delete an event send me the Exact event name.'
	query = update.callback_query
	context.bot.send_message(chat_id=update.effective_chat.id,text=text)
	return DELETING

def deleting(update, context):
	Name = update.message.text
	db.delete_item(Name)
	context.bot.send_message(chat_id=update.effective_chat.id, text= 'Event successfully deleted!')
	return ConversationHandler.END

def typing(update, context):
	message = (update.message.text).split(',')
	Name = message[0]
	DATE = message[1]
	db.add_item(Name, DATE)
	context.bot.send_message(chat_id=update.effective_chat.id, text='Event successfully added!')
	return ConversationHandler.END


def timetable(update, context):
	keyboard_tt = [[InlineKeyboardButton("A", callback_data=str(DIVA)),
				 InlineKeyboardButton("B", callback_data=str(DIVB)),
				 InlineKeyboardButton("C", callback_data=str(DIVC)),
				 InlineKeyboardButton("D", callback_data=str(DIVD))]]

	reply_markup_tt = InlineKeyboardMarkup(keyboard_tt)
	update.message.reply_text('Select your division:', reply_markup=reply_markup_tt)
	return FIRST

def diva(update, context):
	tt_ida = 'https://i.imgur.com/suyQYXA.jpg'
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=tt_ida)
	return ConversationHandler.END

def divb(update, context):
	tt_idb = 'https://i.imgur.com/Ji1RBmR.jpg'
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=tt_idb)
	return ConversationHandler.END

def divc(update, context):
	tt_idc = "https://imgur.com/YuE97bi.jpg"
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=tt_idc)
	return ConversationHandler.END

def divd(update, context):
	tt_idd = "https://i.imgur.com/YjLIBnf.jpg"
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=tt_idd)
	return ConversationHandler.END

def view(update, context):
	v = update.effective_user.id
	j = db.getitems(v)
	text = 'Your attendance Percentage is: ' + str(j)+"%"
	context.bot.send_message(chat_id=update.effective_chat.id, text = text)

def attendance(update, context):
	"""Sends a predefined poll"""
	questions = ["Physics", "Chemistry", "Maths", "CPrograming"]
	message = context.bot.send_poll(update.effective_user.id, "Mark Your attendance", questions,
									is_anonymous=False, allows_multiple_answers=True)
	# Save some info about the poll the bot_data for later use in receive_poll_answer
	payload = {message.poll.id: {"questions": questions, "message_id": message.message_id,
								 "chat_id": update.effective_chat.id, "answers": 0}}
	context.bot_data.update(payload)


def receive_poll_answer(update, context):
	"""Summarize a users poll vote"""
	answer = update.poll_answer
	poll_id = answer.poll_id
	try:
		questions = context.bot_data[poll_id]["questions"]
	# this means this poll answer update is from an old poll, we can't do our answering then
	except KeyError:
		return
	selected_options = answer.option_ids
	answer_string = ""
	for question_id in selected_options:
		if question_id != selected_options[-1]:
			answer_string += questions[question_id] + " and "
		else:
			answer_string += questions[question_id]
	user_mention = mention_html(update.effective_user.id, update.effective_user.full_name)
	context.bot.send_message(context.bot_data[poll_id]["chat_id"],
							 "{} Has Attended {}!. Select /view to view your attendance".format(user_mention, answer_string),
							 parse_mode=ParseMode.HTML)
	context.bot_data[poll_id]["answers"] += 1
	v = update.effective_user.id
	for i in selected_options:
		if (i==0):
			db.updatep(v)
			db.updatelec(v)
		if (i==1):
			db.updatec(v)
			db.updatelec(v)

		if (i==2):
			db.updatem(v)
			db.updatelec(v)

		if (i==3):
			db.updatecp(v)
			db.updatelec(v)
	db.updateall(v)
	db.percent(v)

def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():


	TOKEN = os.environ['TELEGRAM_TOKEN']
	PORT = int(os.environ['PORT'])
	updater = Updater(TOKEN, use_context=True)
	# add handlers
	updater.start_webhook(listen="0.0.0.0",
								port=PORT)
					
	updater.bot.set_webhook("Your_app_url")
	updater.dispatcher.add_error_handler(error)
	
	db.setup()
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('about', about))
	dp.add_handler(CommandHandler('attendance', attendance))
	dp.add_handler(CommandHandler('view', view))
	dp.add_handler(PollAnswerHandler(receive_poll_answer))
	conv_handler = ConversationHandler(
			entry_points=[CommandHandler('timetable', timetable), CommandHandler('event', event), CommandHandler('experiment', experiment), CommandHandler('pdfview', pdfview)],

			states={
				FIRST: [CallbackQueryHandler(diva, pattern='^' + str(DIVA) + '$'),
					CallbackQueryHandler(divb, pattern='^' + str(DIVB) + '$'),
					CallbackQueryHandler(divc, pattern='^' + str(DIVC) + '$'),
					CallbackQueryHandler(divd, pattern='^' + str(DIVD) + '$')],
				SECOND: [CallbackQueryHandler(add_event, pattern='^' + str(addevent) + '$'),
					CallbackQueryHandler(delete_event, pattern='^' + str(delevent) + '$'),
					CallbackQueryHandler(list_event, pattern='^' + str(listevent) + '$')],
				TYPING: [MessageHandler(Filters.text, typing)],
				DELETING: [MessageHandler(Filters.text, deleting)],
				EXP: [CallbackQueryHandler(Physics, pattern='^' + str(Phy) + '$'),
					CallbackQueryHandler(Chemistry, pattern='^' + str(Chem) + '$'),
					CallbackQueryHandler(CPrograming, pattern='^' + str(CP) + '$'),
					CallbackQueryHandler(EngineeringDrawing, pattern='^' + str(ED) + '$')]
	

			},
			fallbacks=[CommandHandler('start', start)]
			)
	mail_handler = ConversationHandler(
		entry_points=[CommandHandler('pdfview', pdfview)],

		states={
			THIRD: [CallbackQueryHandler(SendDocument, pattern='^' + str(sendpdf) + '$'),
					CallbackQueryHandler(MailDocument, pattern='^' + str(mailpdf) + '$')],
			FOURTH: [CallbackQueryHandler(updateemail, pattern='^' + 'update' + '$'),
					 CallbackQueryHandler(sendmail, pattern='^' + 'send' + '$')],
			MAILING: [MessageHandler(Filters.text, mailing)]

		},
		fallbacks=[CommandHandler('start', start)]
		)
	dp.add_handler(mail_handler)

	dp.add_handler(conv_handler)
	 # Start the Bot
	updater.start_polling()


	updater.idle()


if __name__ == '__main__':
	main()
	


	