from flask import Flask, request, make_response, Response
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from sklearn.ensemble import VotingClassifier
import pickle
import xlwt
# import helper
import utilities
import requests
import json
import os

heart_model = 'saved_model.sav'
diab_model = 'diab_model.sav'
app = Flask(__name__)

#slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_signing_secret = 'ENTER_YOUR_SIGNINIG_SECRET_HERE'
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events", app)

#slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_bot_token = 'ENTER_YOUR_BOT_TOKEN_HERE'
slack_client = SlackClient(slack_bot_token)

botUsername = 'test_bot'

users = slack_client.api_call('users.list')
users = users['members']
for user in users:
    if 'name' in user and botUsername in user.get('name') and not user.get('deleted'):
        botID = user.get('id')

botAtID = '<@'+botID+'>'

pvals = []
dvals = []

def predict_model(pickle_file, l):
    loaded_model = pickle.load(open(pickle_file, 'rb'))
    return loaded_model.predict(l)[0]

def show_dialog(dialog_content, channel, trigger_id):
	slack_client.api_call("dialog.open", dialog=dialog_content, trigger_id=trigger_id)

def create_xls(user_name, age, sex, disease_name, predicted_val):
    row1 = ['Username', 'Age', 'Sex', 'Disease', 'Possibility of Disease']
    book = xlwt.Workbook()
    xl_sheet = book.add_sheet(disease_name + ' Report')
    for i in range(5):
        xl_sheet.write(0, i, row1[i])
    sex_fm = 'Male' if sex == 1 else 'Female'
    pred = 'High!' if predicted_val == 1 else 'Low'
    row2 = [user_name, age, sex_fm, disease_name, pred]
    for i in range(4):
        xl_sheet.write(1, i, row2[i])
    if pred == 'Low':
        style = xlwt.easyxf('font: bold 1, color green;')
    else:
        style = xlwt.easyxf('font: bold 1, color red;')
    xl_sheet.write(1, 4, row2[4], style)
    book.save(disease_name + '.xls')

@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    form_json = json.loads(request.form["payload"])
    user = form_json["user"]["id"]
    user_name = form_json["user"]["name"]
    channel = form_json["channel"]["id"]
    actions = form_json.get('actions')
    trigger_id = form_json.get('trigger_id')

    if actions:
        actions = actions[0]
        if actions.get("value") == "heart_disease":
            # helper.show_dialog(utilities.heart_disease_dialog, channel, trigger_id)
            show_dialog(utilities.heart_disease_dialog_1, channel, trigger_id)

        if actions.get("value") == "diabetes":
            # helper.show_dialog(utilities.diabetes_dialog, channel, trigger_id)
            show_dialog(utilities.diabetes_dialog, channel, trigger_id)

        if actions.get("value") == "options":
            # helper.show_dialog(utilities.options_dialog, channel, trigger_id)
            show_dialog(utilities.options_dialog, channel, trigger_id)

        if actions.get("value") == "more_info":
            # helper.show_dialog(utilities.options_dialog, channel, trigger_id)
            show_dialog(utilities.heart_disease_dialog_2, channel, trigger_id)

    if form_json.get("type") == "dialog_submission":
        # callback_id = form_json.get('callback_id')
        if form_json.get('callback_id') == 'heart_disease_1':
            submission = form_json.get('submission')
            global pvals
            if len(pvals) == 0:
                pvals.extend([int(submission['age']), int(submission['sex']), int(submission['chest-pain']), int(submission['blood-pressure']), int(submission['cholesterol']), int(submission['blood-sugar']), int(submission['ecg']), int(submission['max-heart-rate']), int(submission['exercise-angina'])])
            else:
                pvals = []
                pvals.extend([int(submission['age']), int(submission['sex']), int(submission['chest-pain']), int(submission['blood-pressure']), int(submission['cholesterol']), int(submission['blood-sugar']), int(submission['ecg']), int(submission['max-heart-rate']), int(submission['exercise-angina'])])
            print(pvals)
            text_message = "<@{}>\n*We require some more specific information about diagnosis from you:*".format(user)
            slack_client.api_call("chat.postEphemeral", user=user, channel=channel, text=text_message, blocks=utilities.more_info_block, attachments=[])

        elif form_json.get('callback_id') == 'heart_disease_2':
            print('callback 2')
            submission = form_json.get('submission')
            pvals.extend([float(submission['oldpeak']), int(submission['slope']), int(submission['ca']), int(submission['thal'])])
            predicted_val = predict_model(heart_model, [pvals])
            if predicted_val == 1:
                prediction_text = "Possibility of heart disease => *HIGH!*\nPLEASE CONSULT A DOCTOR IMMEDIATELY!"
            else:
                prediction_text = "Possibility of heart disease => *LOW*"
            slack_client.api_call("chat.postMessage", channel=channel, text="<@{}>\n```{}```".format(user, prediction_text))
            create_xls(user_name, pvals[0], pvals[1], 'Heart_Disease', predicted_val)
            slack_client.api_call("files.upload", channels=channel, file=open('Heart_Disease.xls', 'rb'), initial_comment="*Here's your report: *",title='Heart_Disease_Report')


        elif form_json.get('callback_id') == 'diabetes':
        	submission = form_json.get('submission')
        	global dvals
        	if len(dvals) == 0:
        		dvals.extend([int(submission['pregnancies'].split('-')[1]), int(submission['glucose-level']), int(submission['blood-pressure']), int(submission['skin-thk']), int(submission['insulin-level']), float(submission['bmi']), float(submission['dpf']), int(submission['age'])])
        	else:
        		dvals = []
        		dvals.extend([int(submission['pregnancies'].split('-')[1]), int(submission['glucose-level']), int(submission['blood-pressure']), int(submission['skin-thk']), int(submission['insulin-level']), float(submission['bmi']), float(submission['dpf']), int(submission['age'])])
        	print(dvals)
        	predicted_val = predict_model(diab_model, [dvals])
        	if predicted_val == 1:
        		prediction_text = "Possibility of diabetes => *HIGH!*\nPLEASE CONSULT A DOCTOR IMMEDIATELY!"
        	else:
        		prediction_text = "Possibility of diabetes => *LOW*"
        	slack_client.api_call("chat.postMessage", channel=channel, text="<@{}>\n```{}```".format(user, prediction_text))
        	create_xls(user_name, dvals[7], int(submission['sex']), 'Diabetes', predicted_val)
        	slack_client.api_call("files.upload", channels=channel, file=open('Diabetes.xls', 'rb'), initial_comment="*Here's your report: *",title='Diabetes_Report')
        
        #submission = form_json.get('submission')

        # if callback_id == 'diabetes':
        #     month_duration = int(submission['duration'].split('-')[0])
        #     start_date, end_date = utilities.get_dates(month_duration)
        #     submission['start_date'] = start_date
        #     submission['end_date'] = end_date

            # if submission.get('report'):
            #     file_name = submission.get('report')+'.txt'
            #     slack_client.api_call("files.upload", channels=channel, file=open(file_name, 'rb'), \
            #                     initial_comment="*Here's your file: *",title=file_name)

        # helper.redis_set(user, callback_id, submission)
        # slack_client.api_call("chat.postMessage", channel=channel, text="Okay <@"+user+">, we are working on your report and will update you shortly.")

    return make_response("", 200)

@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and botAtID in message.get('text'):
        user = message["user"]
        channel = message["channel"]
        text_message = "Hi <@%s>! " % user
        blocks=[
    {
    	"type": "section",
    	"text": {
    		"type": "mrkdwn",
    		"text": "Hi <@{}>!\n*I can help you in diagnosing any of the following:*".format(user)
    		}
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Heart Disease"
                },
                "style": "primary",
                "value": "heart_disease"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Diabetes"
                },
                "style": "primary",
                "value": "diabetes"
            }
        ]
    }
]
        slack_client.api_call("chat.postEphemeral", user=user, channel=channel, text=text_message, blocks=blocks, attachments=[])

# @slack_events_adapter.on("file_shared")
# def handle_file(event_data):
#     message = event_data["event"]
#     user = message["user_id"]
#     channel = message["channel_id"]
#     file_id = message["file_id"]
#     file_info = slack_client.api_call("files.info", file=file_id)
#     report_name = file_info["file"]["name"].replace(".txt", "")
#     if user == botID:
#         slack_client.api_call("chat.postMessage", user=user, channel=channel, text='```File ID = '+file_id+'```')
#         helper.redis_shared_files(report_name, file_id)

# @slack_events_adapter.on("error")
# def error_handler(err):
#     print("ERROR: " + str(err))

# def delete_file(redis_key):
#     file_id = redis_key.split(':')[1]
#     response = slack_client.api_call("files.delete", file=file_id)
#     if response["ok"] == True:
#         helper.redis_delete(redis_key)

if __name__=='__main__':
    app.run(port=3000)
    #app.run(host='0.0.0.0', port=80)