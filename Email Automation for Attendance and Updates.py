#!/usr/bin/env python
# coding: utf-8

# # EMAIL AUTOMATION FOR ATTENDANCE AND UPDATES

# In[9]:


import os
from email.message import EmailMessage
import ssl
import smtplib
#standard technology for keeping the internet connection safe and secure
email_sender= 'anshtandon1503@gmail.com'
email_password=os.environ.get("EMAIL_PASSWORD")
email_receiver='ap6277@srmist.edu.in'


# # SUBJECT AND BODY OF EMAIL

# In[10]:


subject='Absentees on the date 26/1/23 are:'
body=""""
In regards to the the above subject the absentees for the following marked sessions are given below
"""


# # SETTING AN OBJECT FOR EMAIL WRITTING

# In[11]:


em=EmailMessage()
em['From']=email_sender
em['To']=email_receiver
em['Subject']=subject
em.set_content(body)


# # CONTEXT SETTING

# In[13]:


context=ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context )as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender,email_receiver,em.as_string())


# In[ ]:




