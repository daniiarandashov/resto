from django.contrib import auth
from django.db.models import query
from django.http import request
from .models import Feedback,Comment
from django.shortcuts import render,redirect
from .forms import UserRegistration
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


########################################################################
######################## Rest Imports ##################################
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer, UserSerializer,User,FeedbackSerializer
########################################################################


def index(request):
    '''Функция index возвращает HTML главной страницы'''
    return render(
        request=request,
        template_name='main/index.html'
    )

def about(request):
    '''Функция about возвращает HTML страницу о компании'''
    return render(
        request=request,
        template_name='main/about.html'
    )

def registration(request):
    '''Функция registration возвращает HTML для регистрации'''
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

        else:
            return render(
            request=request,
            template_name='main/registration.html',
            context={"form":form}
            )
    else:
        form = UserRegistration()
        return render(
            request=request,
            template_name='main/registration.html',
            context={"form":form}
            )

def feedbacks(request):
    all_feedbacks = Feedback.objects.all()
    return render(
        request=request,
        template_name='main/feedbacks.html',
        context={"all_feedbacks":all_feedbacks}
    )


class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ('feedback_text',)
    template_name = 'main/feedback_create.html'

    def get_context_data(self, **kwargs):
        kwargs["feedbacks"] = Feedback.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

class FeedbackDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Feedback
    template_name = 'main/feedback_detail.html'

    def get_context_data(self, **kwargs):
        feedback = self.get_object()
        kwargs["comments"] = Comment.objects.filter(author=feedback.pk)
        return super().get_context_data(**kwargs)




class FeedbackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    fields = ('feedback_text',)
    template_name = 'main/feedback_detail.html'

    def get_context_data(self, **kwargs):
        feedback = self.get_object()
        kwargs['feedbacks'] = Feedback.objects.get(pk=feedback.pk)
        kwargs['comments'] = Comment.objects.filter(assigned_to_feedback=feedback.pk)
        return super().get_context_data(**kwargs)


    def test_func(self):
        feedback = self.get_object()

        if self.request.user == feedback.author:
            return True
        return False



class FeedbackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Feedback
    template_name = 'main/feedback_delete.html'
    success_url ='/feedbacks/'

    
    def test_func(self):
        feedback = self.get_object()

        if self.request.user == feedback.author:
            return True
        return False


#####################################################################################################
###################################### DJANGO REST VIEWS ############################################
#####################################################################################################

# class UserListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def get(self,request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)

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
                "result":"Неверно"
            },
            status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

        serializer = UserSerializer(data=request.data,context = {
            "user_id":user_id,
            "request":request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Пользователь был создан успешно"
            },
            status = status.HTTP_201_CREATED
        )

class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def put(self,request):
        try:
            user_id = User.objects.get(pk=request.data.get('user_id'))

            serializer = UserSerializer(
                instance=user_id,
                data=request.data,
                partial = True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
            data={
                "success":True,
                "result":"Пользователь был ОБНОВЛЕН успешно"
            },
            status = status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Пользователь не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def delete(self,request):
        try:
            user_id = User.objects.get(pk=request.data.get('user_id'))
            user_id.delete()
            # print(user_id.feedback_text)
            return Response(
            data={
                "success":True,
                "result":"ПОЛЬЗОВАТЕЛЬ был DELETED успешно"
            },
            status = status.HTTP_202_ACCEPTED
            )
        except User.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"ПОЛЬЗОВАТЕЛЬ не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

# class FeedbackListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     serializer_class = FeedbackSerializer
    
#     def get_queryset(self):
#         queryset = Feedback.objects.all()
#         return queryset

class FeedbackCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = FeedbackSerializer

    def get(self,request):
        feedbacks = Feedback.objects.all()
        serializer = self.serializer_class(feedbacks, many=True)

        return Response(
            data={
                "success":True,
                "result":serializer.data
            },
            status=status.HTTP_200_OK
        )
        

    def post(self, request):
        try:
            if request.data.get('author_id'):
                user = User.objects.get(pk=request.data.get('author_id'))
                author_id = user.pk
            else:
                author_id = None
        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя не существует"
            },
            status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

        serializer = FeedbackSerializer(data=request.data,context = {
            "author_id":author_id,
            "request":request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Отзыв был оставлен успешно"
            },
            status = status.HTTP_201_CREATED
        )

class FeedbackUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer

    def put(self,request):
        try:
            feedback_id = Feedback.objects.get(pk=request.data.get('feedback_id'))

            serializer = FeedbackSerializer(
                instance=feedback_id,
                data=request.data,
                partial = True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
            data={
                "success":True,
                "result":"Отзыв был ОБНОВЛЕН успешно"
            },
            status = status.HTTP_200_OK
            )
        except Feedback.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Отзыв не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )
        
class FeedbackDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer

    def delete(self,request):
        try:
            feedback_id = Feedback.objects.get(pk=request.data.get('feedback_id'))
            feedback_id.delete()
            print(feedback_id.feedback_text)
            return Response(
            data={
                "success":True,
                "result":"Отзыв был DELETED успешно"
            },
            status = status.HTTP_202_ACCEPTED
            )
        except Feedback.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Отзыв не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )


# class CommentListAPIView(generics.ListAPIView):
#     permission_classes = [AllowAny,]
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()

class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CommentSerializer

    def get(self,request):
        comments = Comment.objects.all()
        serializer = self.serializer_class(comments, many=True)

        return Response(
            data={
                "success":True,
                "result":serializer.data
            },
            status=status.HTTP_200_OK
        )
        

    def post(self, request):
        try:
            if request.data.get('author_2_id'):
                user = User.objects.get(pk=request.data.get('author_2_id'))
                author_2_id = user.pk
            else:
                author_2_id = None
        except User.DoesNotExist:
            return Response(
            data={
                "success":False,
                "result":"Такого пользователя не существует"
            },
            status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

        serializer = CommentSerializer(data=request.data,context = {
            "author_2_id":author_2_id,
            "request":request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "success":True,
                "result":"Комментарий был оставлен успешно"
            },
            status = status.HTTP_201_CREATED
        )

class CommentUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer

    def put(self,request):
        try:
            comment_id = Comment.objects.get(pk=request.data.get('comment_id'))

            serializer = CommentSerializer(
                instance=comment_id,
                data=request.data,
                partial = True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
            data={
                "success":True,
                "result":"Комментарий был ОБНОВЛЕН успешно"
            },
            status = status.HTTP_200_OK
            )
        except Comment.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Комментарий не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

class CommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer

    def delete(self,request):
        try:
            comment_id = Comment.objects.get(pk=request.data.get('comment_id'))
            comment_id.delete()
            # print(comment_id.comment_text)
            return Response(
            data={
                "success":True,
                "result":"Комментарий был DELETED успешно"
            },
            status = status.HTTP_202_ACCEPTED
            )
        except Comment.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Комментарий не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )