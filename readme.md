# Chat App 


## Description 
    . Basic chat app to make one-to-one conversation between the agents and the client.
    

## Pre-Requisite to install 
    . Python==3.9.13
    . virutualenv venv
    . pip install -r requirements.txt


### Automatic                             -           Manual in setting.py under database 
    . install docker if not already setup           . USER = "postgres"  / can be of your own 
                                                      preference as well
    . `docker-compose up --build`                   . NAME = "chat_app"  / can be of your own 
                                                      preference as well
                                                    . PASSWORD = "postgres"  / can be of your own 
                                                      preference as well
                                                    . HOST = "localhost"
                                                    . PORT = 5432

### Migration command to be done in Database
    . python manage.py makemigrations
    . python manage.py migrate

### Run server directly
    . python manage.py runserver

### Start Redis for webSocket 
    . run in terminal :
        `docker run -p 6379:6379 -d redis:5`
    

### To check if connection is running with redis    (Not Mandatory)
    $ python3 manage.py shell
    >>> import channels.layers
    >>> channel_layer = channels.layers.get_channel_layer()
    >>> from asgiref.sync import async_to_sync
    >>> async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
    >>> async_to_sync(channel_layer.receive)('test_channel')
    {'type': 'hello'}


## API's:

.To Create User:

    `http://127.0.0.1:8000/chat-app/user/`   
        Form data : 
            . Username
            . Password
            . role

.To Delete User:

    `http://127.0.0.1:8000/chat-app/user/<int:pk>/`
        Param:
            . pk = user's id

.To Create a thread, send message only done by client:

    `http://127.0.0.1:8000/chat-app/send-message/`
        Form data :
            . Username
            . Password
            . Message_body
            . Thread_type

.To get Message-list:

    For client:                                               
        `http://127.0.0.1:8000/chat-app/message-list/`       
        Form data:                                             
            . Username                                             
            . Password                                             
            . Thread_type 

    For Agent:     
        `http://127.0.0.1:8000/chat-app/message-list/` 
    Form data:
        .Username
        .Password


. To get all the conversations between Client and Agent:

    `http://127.0.0.1:8000/chat-app/thread-list/`
    Form data:
        . Agent_id
        . Client_id

. To connect in chat for Agents and Client:

    Connect in two different browsers:
        `http://127.0.0.1:8000/chat-app/<int:thread_id>/<int:user_id>`




## Extra Features included:
    . Prevent multiple agents working on the same message at once.
    . Explore ways to surface messages that are more urgent and in need of immediate attention. 





