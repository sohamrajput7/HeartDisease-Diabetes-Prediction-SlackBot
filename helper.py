from slackclient import SlackClient
# import redis
import json
import utilities

#slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_bot_token = 'ENTER_YOUR_BOT_TOKEN_HERE'
slack_client = SlackClient(slack_bot_token)

# redis_db = redis.Redis(host='localhost', port=6379, db=0)

# def show_dialog(dialog_content, channel, trigger_id):
# 	slack_client.api_call("dialog.open", dialog=dialog_content, trigger_id=trigger_id)

# def redis_set(user, callback_id, submission):
# 	key = user+'_'+callback_id+'_query'
# 	if redis_db.get(key):
# 		submission_value = json.loads(redis_db.get(key))
# 		submission_value.append(submission)
# 	else:
# 		submission_value = []
# 		submission_value.append(submission)
# 	redis_db.set(key, json.dumps(submission_value))

# def redis_shared_files(report_name, file_id):
# 	key = report_name+':'+file_id
# 	submission_value = {'date_created': utilities.TODAY.strftime('%Y-%m-%d')}
# 	if not redis_db.get(key):
# 		redis_db.set(key, json.dumps(submission_value))

# def file_delete(redis_key):
# 	file_id = redis_key.split(':')[1]
# 	slack_client.api_call("files.delete", file=file_id)

# def redis_delete(redis_key):
# 	redis_db.delete(redis_key)
	
# def redis_get(user):
# 	return json.loads(redis_db.get(user+' something'))