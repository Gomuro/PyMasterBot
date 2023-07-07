#One-time Training Reminder Template
one_time_template = """
Subject: Training Reminder: {training_name} on {training_date} at {training_time}

Hi {participant_name}!!,

Heads-up about the super exciting training session coming up on {training_date} at {training_time}. 
We can't wait to see you there for the awesome {training_name}!
"""

#Recurring Training Reminder Template
recurring_template = """
Subject: Training Reminder: {training_name} on {training_days} at {training_time}

Hi {participant_name}!!,

We hope you're enjoying the ongoing training sessions for {training_name}. The upcoming sessions are scheduled for {training_days} at {training_time}. We can't wait to see you there.
"""

#Training Is Ready Template
is_ready_template = """
Hi {participant_name}!!,

Your {training_name} is ready. We can't wait to see you there.

"""
#Feedback Template
feedback_template ="""
Hi {participant_name}!!,

Hope you enjoyed {training_name}. Tell us about your experience!!

"""

template_values = {
    'training_name': '',
    'training_date': '',
    'training_time': '',
    'training_days': '',
    'participant_name': '',
    
}
#Customize the template and send the notification
one_time_notification = one_time_template.format(**template_values)
recurring_notification = recurring_template.format(**template_values)
is_ready_notifiation = is_ready_template.format(**template_values)
feedback_notification = feedback_template.format(**template_values)