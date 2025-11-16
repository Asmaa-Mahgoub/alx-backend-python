from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    
    # Choose serializer dynamically
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    # Optional: custom endpoint to add a message directly in conversation
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not sender_id or not message_body:
            return Response(
                {"error": "sender_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid sender_id"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # Optional: filter messages by conversation
    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return self.queryset.filter(conversation__conversation_id=conversation_id)
        return self.queryset
    

