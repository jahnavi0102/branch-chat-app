"""
Script to load the csv data in the database
"""
import pandas as pd
from chat_app.models import User, Message, Thread
from datetime import datetime

message_df = pd.read_csv('message_data.csv')
df = pd.DataFrame(message_df)

id =0
df["priority"] = ""
for index, row in df.iterrows(): 
    # dates = datetime.strptime(str(row["Timestamp (UTC)"]), "%Y-%m-%d %H:%M:%S"),
    message = row["Message Body"]
    if "payment" and "loan" in message:
        priority = 1
    elif "payment" and not "loan" in message:
        priority = 2
    elif "loan" in message:
        priority = 1
    else:
        priority = 3
    df.at[index,"priority"] = priority

df2 = df.groupby('User ID')[['Timestamp (UTC)', 'priority']].min()
dicts = {}
for index, row in df2.iterrows():
    dates = datetime.strptime(str(row["Timestamp (UTC)"]), "%Y-%m-%d %H:%M:%S"),
    dicts[str(index)] = {"timestamp":dates, "priority":row["priority"]}

for index, row in df.iterrows():
    username = str(row["User ID"])
    message = row["Message Body"]
    timestamp = row["Timestamp (UTC)"]
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        thread = Thread.objects.get(client_id=user.id)
        message = Message(thread_id = thread.id, sender_id = user.id,message_body=message, timestamp=timestamp)
        message.save()
    
    else:
        user = User(username=username, password=username, role="client")
        user.save()
        thread = Thread(client_id = user.id, start_time=dicts[username]["timestamp"], thread_type = dicts[username]["priority"])
        thread.save()
        message = Message(thread_id = thread.id, sender_id = user.id,message_body=message, timestamp=timestamp)
        message.save()

print("Data uploaded")
    