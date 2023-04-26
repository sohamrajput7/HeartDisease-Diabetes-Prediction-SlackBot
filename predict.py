from sklearn.ensemble import VotingClassifier

def predict(pickle_file, l):
	loaded_model = pickle.load(open(pickle_file, 'rb'))
	return loaded_model.predict(l)[0]

pickle_file = 'saved_model.sav'
#l=[[58,0,0,130,40,0,1,131,0,0.6,1,0,2]]
vals = [58, 0, int(submission['chest-pain']), int(submission['blood-pressure']), int(submission['cholesterol']), int(submission['blood-sugar']), int(submission['ecg']), int(submission['max-heart-rate']), int(submission['exercise-angina']), 0.6,1,0,2]
l = [vals]
predict(pickle_file, l)
#index_= ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']