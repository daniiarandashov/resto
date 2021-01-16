from django.shortcuts import render
from django.views.generic import ListView,CreateView
from .models import Cook

########################################################################
######################## Rest Imports ##################################
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CookSerializer
from django.contrib.auth.models import User
########################################################################

class CookCreateView(CreateView):
    model = Cook
    fields = ('user','position','education','experience','history_of_work')
    template_name =  'teams/team.html'

    def get_context_data(self, **kwargs):
        kwargs["cook"]= Cook.objects.all()
        return super().get_context_data(**kwargs)

#####################################################################################################
###################################### DJANGO REST VIEWS ############################################
#####################################################################################################

class CookCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CookSerializer

    def get(self,request):
        cooks = Cook.objects.all()
        serializer = self.serializer_class(cooks, many=True)

        return Response(
            data={
                "success":True,
                "result":serializer.data
            },
            status=status.HTTP_200_OK
        )
        

    def post(self, request):
        try:
            if request.data.get('user_id'):
                user = User.objects.get(pk=request.data.get('user_id'))
                user_id = user.pk
            else:
                user_id = None
        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя не существует"
            },
            status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

        serializer = CookSerializer(data=request.data,context = {
            "user_id":user_id,
            "request":request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Повар был успешно добавлен"
            },
            status = status.HTTP_201_CREATED
        ) 

class CookUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CookSerializer

    def put(self,request):
        try:
            user_id = Cook.objects.get(pk=request.data.get('user_id'))

            serializer = CookSerializer(
                instance=user_id,
                data=request.data,
                partial = True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
            data={
                "success":True,
                "result":"Данные были ОБНОВЛЕНЫ успешно"
            },
            status = status.HTTP_200_OK
            )
        except Cook.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Повар не найдена!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

class CookDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CookSerializer

    def delete(self,request):
        try:
            user_id = Cook.objects.get(pk=request.data.get('user_id'))
            user_id.delete()
            # print(comment_id.comment_text)
            return Response(
            data={
                "success":True,
                "result":"Повар был DELETED успешно"
            },
            status = status.HTTP_202_ACCEPTED
            )
        except Cook.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Повар не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )