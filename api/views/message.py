from django.db.models import Q
from django.forms import model_to_dict
from django.urls import path
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from api.models import User, Message


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_message_api(request: Request) -> Response:
    receiver_identifier = request.data['receiver']
    receiver = User.objects.filter(Q(username=receiver_identifier) | Q(email=receiver_identifier)).first()
    if receiver is None:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    subject = request.data['subject']
    message = request.data['message']
    message = Message.objects.create(sender=request.user, receiver=receiver, message=message, subject=subject)
    return Response(f'message {message.id}  created successfully')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_messages_api(request: Request) -> Response:
    messages = list(Message.objects.filter(receiver=request.user)
                    .values('id', 'sender', 'subject', 'message', 'created_at')
                    .order_by('created_at')
                    .all())
    return Response(messages)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_unread_messages_api(request: Request) -> Response:
    messages = list(Message.objects.filter(receiver=request.user, read=False)
                    .values('id', 'sender', 'subject', 'message', 'created_at')
                    .order_by('created_at')
                    .all())
    return Response(messages)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def read_message_api(request: Request) -> Response:
    message_id = request.data.get('message_id', None)
    if message_id:
        message = Message.objects.filter(receiver=request.user, read=False, id=message_id).first()
    else:
        message = Message.objects.filter(receiver=request.user, read=False).order_by('created_at').first()
    if not message:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    message.read = True
    message.save()
    message = model_to_dict(instance=message, fields=['id', 'sender', 'subject', 'message', 'created_at'])
    return Response(message)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_received_message_api(request: Request) -> Response:
    message_id = request.data.get('message_id', None)
    if message_id:
        message = Message.objects.filter(receiver=request.user, id=message_id).first()
    else:
        message = Message.objects.filter(receiver=request.user).order_by('created_at').first()
    if not message:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    message_id = message.id
    message.delete()
    return Response(f'Message {message_id} deleted successfully')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_sent_message_api(request: Request) -> Response:
    message_id = request.data.get('message_id', None)
    if message_id:
        message = Message.objects.filter(sender=request.user, id=message_id).first()
    else:
        message = Message.objects.filter(sender=request.user).order_by('created_at').first()
    if not message:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    message_id = message.id
    message.delete()
    return Response(f'Message {message_id} deleted successfully')


message_urls = [
    path('message/send_message/', send_message_api),
    path('message/read_message/', read_message_api),
    path('message/delete_recevied_message/', delete_received_message_api),
    path('message/delete_sent_message/', delete_sent_message_api),
    path('message/get_all_messages/', get_all_messages_api),
    path('message/get_unread_messages/', get_unread_messages_api),

]
