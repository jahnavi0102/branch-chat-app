"""
All the views of the apps are listed here. 
"""
from rest_framework import viewsets
from .models import User, Message, Thread
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.core.exceptions import ValidationError
from django.shortcuts import render

class UserViewSet(viewsets.ViewSet):
    """
    All the views of the USERS are listed here. 
    """
    def create(self, request):
        try:
            if not (request.data.get("username") and request.data.get("password") and request.data.get("role")):
                message = {"error":"'username', 'password' and 'role' is a must"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            username = request.data["username"]
            if User.objects.filter(username=username).exists():
                message = {"error":f"{username} already exists"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer = UserSerializer(data=request.data)
            except ValidationError as error:
                return Response(str(error), status=status.HTTP_406_NOT_ACCEPTABLE)
            if serializer.is_valid():
                user = User(**serializer.validated_data)
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                message = {"error": "validation error"}
                return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            User.objects.get(pk=pk)
        except User.DoesNotExist:
            message = ({"error":f"Id doesn't exist"})
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            if User.objects.filter(pk=pk, is_deleted = True).exists():
                message = ({"error":f"Id doesn't exist"})
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
            user = User.objects.get(id=pk)
            user.is_deleted = True
            user.save()
            message = {"deleted": "User is deleted successfully"}
            return Response(message, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageViewSet(viewsets.ViewSet):
    """
    All the views of the MESSAGE are listed here. 
    """
    def list(self, request):
        try:
            if not (request.data.get("username") and request.data.get("password")):
                message = {"error":"'username' and 'password' is a must"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            username = request.data["username"]
            password = request.data["password"]
            try:
                user = User.objects.get(username=username, password=password, is_deleted=False)
            except User.DoesNotExist:
                message = {"missing": f"Either password is wrong or {username} doesn't exist"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if user.role == "AGENT":
                thread = list(Thread.objects.filter(agent=None).order_by('thread_type')[:11])
                all_messages = Message.objects.filter(thread__in=thread, is_read=False).order_by('sender').distinct('sender')         
                all_message=[]
                for message in all_messages:
                    get_message={}
                    get_message["message"] =  message.message_body
                    get_message["client_id"] = message.sender.id
                    get_message["timestamp"] = message.timestamp
                    get_message["is_read"] = message.is_read
                    all_message.append(get_message)
                message = {"chats_recieved":all_message}
                return Response(message, status=status.HTTP_200_OK)

            elif user.role == "client":
                if not request.data.get("thread_type"):
                    message = {"missing": "Client must mention the conversation type [1 for loan, 2 for payment, 3 for other]."}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                try:
                    thread = Thread.objects.get(client__username=username, thread_type=request.data["thread_type"])
                except Thread.DoesNotExist:
                    message = {"missing": f"No message has been sent by you."}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                all_messages = tuple(Message.objects.filter(sender__username=username, sender__password=password, is_read=False, thread_id=thread.id))
                if not all_messages:
                    message = {"warning":"You haven't send any messages"}
                    return Response(message, status=status.HTTP_200_OK)
                all_message=[]
                for messages in all_messages:
                    get_messages={}
                    get_messages["message"] =  messages.message_body
                    get_messages["timestamp"] = messages.timestamp
                    get_messages["is_read"] = messages.is_read
                    all_message.append(get_messages)
                message = {"chats_sent":all_message}
                return Response(message, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            if not (request.data.get("username") and request.data.get("password") and request.data.get("message_body") and request.data.get("thread_type")):
                message = {"error":"'username','password' and 'message_body' is a must"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            username = request.data["username"]
            password = request.data["password"]
            message_body = request.data["message_body"]
            thread_type = request.data["thread_type"]
            try:
                user = User.objects.get(username=username, password=password, is_deleted=False)
            except User.DoesNotExist:
                message = {"missing": f"Either password is wrong or {username} doesn't exist"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if not user.role == "client":
                message = {"Invalid": "You cannot send a message, it can only be done by client"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            try:
                thread = Thread.objects.get(client_id=user.id, thread_type=thread_type)
                if not thread.agent_id is None:
                    message = {"Invalid": "You cannot send a message, this thread is closed"}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            except Thread.DoesNotExist:
                thread = Thread(client_id=user.id, thread_type=thread_type)
                thread.save()
            message = Message(sender_id=user.id, message_body=message_body, thread_id = thread.id)
            message.save()
            message = {"chat_sent_successfully":message_body}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThreadViewSet(viewsets.ViewSet):
    """
    All the views of the THREAD are listed here. 
    """
    def list(self, request):
        try:
            if not (request.data.get("client_id") and request.data.get("agent_id")):
                message = {"error":"'client_id' and 'agent_id' is a must"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            
            client_id = request.data["client_id"]
            agent_id = request.data["agent_id"]
            try:
                User.objects.get(pk=agent_id)
                User.objects.get(pk=client_id)
            except User.DoesNotExist:
                message = {"missing": f"Either agent or the client doesn't exist"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            all_messages = tuple(Message.objects.filter(thread__agent__id=agent_id, thread__client__id=client_id).order_by('timestamp'))
            all_message=[]
            for messages in all_messages:
                get_messages={}
                get_messages["message"] =  messages.message_body
                get_messages["timestamp"] = messages.timestamp
                get_messages["is_read"] = messages.is_read
                all_message.append(get_messages)
            message = {"all_conversations":all_message}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


def room(request, pk, user_id):
     return render(request, "chat/room.html", {"pk": pk, "user_id": user_id})      
      

