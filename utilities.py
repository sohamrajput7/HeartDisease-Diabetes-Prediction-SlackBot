# from datetime import date
# from dateutil.relativedelta import relativedelta

# TODAY = date.today()

# def get_platforms():
# 	options = []
# 	for platform in platforms:
# 		mod_platform = platform.lower().replace('- ', '').replace('(', '').replace(')', '').replace(' ', '-')
# 		options.append({"label":  platform, "value": mod_platform})
# 	return options

# def get_regions():
# 	options = []
# 	for region in regions:
# 		# region["text"] = region.pop("name")
# 		# region["value"] = region.pop("code")
# 		options.append({"label": region["name"], "value": region["code"]})
# 	return options

# def get_instance_types():
# 	options = []
# 	for instance in instance_types:
# 		mod_instance = instance.lower()
# 		options.append({"label": instance, "value": mod_instance})
# 	return options

# def get_apns():
# 	options = []
# 	for apn in apns:
# 		mod_apn = apn.split(' ')[0]
# 		options.append({"label": apn, "value": mod_apn})
# 	return options

# def get_dates(month_duration):
#     # TODAY = date.today()
#     relative_date = TODAY + relativedelta(months=-month_duration)
#     start_date = date(relative_date.year, relative_date.month, 1)
#     end_date = start_date + relativedelta(months=+month_duration, days=-1)
#     start_date = start_date.strftime('%Y-%m-%d')
#     end_date = end_date.strftime('%Y-%m-%d')
#     return start_date, end_date

def get_pg():
    options = [{"label": "0 / Not Applicable", "value": "pg-0"}]
    for i in range(1, 11):
        options.append({"label": str(i), "value": "pg-"+str(i)})
    return options

more_info_block=[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*We require some more specific information about diagnosis from you:*"
            }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Enter diagnosis information"
                },
                "style": "primary",
                "value": "more_info"
            }
        ]
    }
]

heart_disease_dialog_1 = {
    "callback_id": "heart_disease_1",
    "state": "show-heart-dialog-1",
    "title": "Diagnose Heart Disease",
    "submit_label": "Submit",
    "elements": 
    [
            {
                "label": "Age",
                "type": "text",
                "name": "age",
                "subtype": "number",
                "placeholder": "(in Years)"
            },
            {
                "label": "Sex",
                "type": "select",
                "name": "sex",
                "options": [
                {
                    "label": "Female",
                    "value": 0
                },
                {
                    "label": "Male",
                    "value": 1
                }
                ]
            },
            {
                "label": "Chest Pain Type",
                "type": "select",
                "name": "chest-pain",
                "options": [
                {
                    "label": "Typical Angina",
                    "value": 0
                },
                {
                    "label": "Atypical Angina",
                    "value": 1
                },
                {
                    "label": "Non-Anginal Pain",
                    "value": 2
                },
                {
                    "label": "Asymptomatic",
                    "value": 3
                }
                ]
            },
            {
                "label": "Blood Pressure",
                "type": "text",
                "name": "blood-pressure",
                "subtype": "number",
                "placeholder": "(in mmHg)"
            },
            {
                "label": "Serum Cholesterol",
                "type": "text",
                "name": "cholesterol",
                "subtype": "number",
                "placeholder": "(in mg/dL)"
            },
            {
                "label": "Fasting Blood Sugar > 120 mg/dL?",
                "type": "select",
                "name": "blood-sugar",
                "options": [
                {
                    "label": "Yes",
                    "value": 1
                },
                {
                    "label": "No",
                    "value": 0
                }
                ]
            },
            {
                "label": "Resting ECG Result",
                "type": "select",
                "name": "ecg",
                "options": [
                {
                    "label": "0 - Normal",
                    "value": 0
                },
                {
                    "label": "1 - Having ST-T wave abnormality",
                    "value": 1
                },
                {
                    "label": "2 - Showing left ventricular Hypertrophy",
                    "value": 2
                }
                ]
            },
            {
                "label": "Max. Heart Rate",
                "type": "text",
                "name": "max-heart-rate",
                "subtype": "number",
                "placeholder": "Maximum Heart Rate"
            },
            {
                "label": "Exercise Induced Angina?",
                "type": "select",
                "name": "exercise-angina",
                "options": [
                {
                    "label": "Yes",
                    "value": 1
                },
                {
                    "label": "No",
                    "value": 0
                }
                ]
            }
    ]
}

heart_disease_dialog_2 = {
    "callback_id": "heart_disease_2",
    "state": "show-heart-dialog-2",
    "title": "Diagnose Heart Disease",
    "submit_label": "Submit",
    "elements": 
    [
            {
                "label": "OldPeak Value",
                "type": "text",
                "name": "oldpeak",
                "subtype": "number",
                "placeholder": "ST wave depression"
            },
            {
                "label": "Slope of ST wave",
                "type": "select",
                "name": "slope",
                "options": [
                {
                    "label": "0 - Up Sloping",
                    "value": 0
                },
                {
                    "label": "1 - Flat",
                    "value": 1
                },
                {
                    "label": "2 - Down Sloping",
                    "value": 2
                },
                ]
            },
            {
                "label": "Fluoroscopy-coloured vessels",
                "type": "text",
                "name": "ca",
                "subtype": "number",
                "placeholder": "0-4"
            },
            {
                "label": "Thal",
                "type": "text",
                "name": "thal",
                "subtype": "number",
                "placeholder": "0-3"
            }
    ]
}

diabetes_dialog = {
    "callback_id": "diabetes",
    "state": "show-diabetes-dialog",
    "title": "Diagnose Diabetes",
    "submit_label": "Submit",
    "elements": 
    [
            {
                "label": "No. of pregnancies (if applicable)",
                "type": "select",
                "name": "pregnancies",
                "options": get_pg()
            },
            {
                "label": "Blood Glucose Level",
                "type": "text",
                "name": "glucose-level",
                "subtype": "number",
                "placeholder": "(in mg/dL)"
            },
            {
                "label": "Blood Pressure",
                "type": "text",
                "name": "blood-pressure",
                "subtype": "number",
                "placeholder": "(in mmHg)"
            },
            {
                "label": "Skin Thickness",
                "type": "text",
                "name": "skin-thk",
                "subtype": "number",
                "placeholder": "Triceps Skin Fold (in mm)"
            },
            {
                "label": "Insulin Level",
                "type": "text",
                "name": "insulin-level",
                "subtype": "number",
                "placeholder": "(in μU/mL)"
            },
            {
                "label": "BMI",
                "type": "text",
                "name": "bmi",
                "subtype": "number",
                "placeholder": "(Weight in kg / (Height in m)^2)"
            },
            {
                "label": "Diabetes Pedigree Function",
                "type": "text",
                "name": "dpf",
                "subtype": "number",
                "placeholder": "Float value"
            },
            {
                "label": "Age",
                "type": "text",
                "name": "age",
                "subtype": "number",
                "placeholder": "(in years)"
            },
            {
                "label": "Sex",
                "type": "select",
                "name": "sex",
                "options": [
                {
                    "label": "Female",
                    "value": 0
                },
                {
                    "label": "Male",
                    "value": 1
                }
                ]
            }
    ]
}

options_dialog = {
    "callback_id": "options",
    "state": "show-options",
    "title": "Other Options",
    "submit_label": "Submit",
    "elements": 
    [
            {
                "label": "Blank",
                "type": "text",
                "name": "account_id",
                "subtype": "number"
            }
    ]
}