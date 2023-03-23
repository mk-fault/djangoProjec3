import json

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from drf import models
from drf.serializers import CourseSerializer

from rest_framework.decorators import api_view,authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication

# Create your views here.
def ip(request):
    return HttpResponse('还能访问')

def ip2(request):
    return HttpResponse('还能访问')

course_list = {
    'name':'课程名称',
    'introduction':'课程介绍',
    'price':0.11
}

@receiver(post_save,sender=settings.AUTH_USER_MODEL) # sender也可以直接写成User
def generate_token(sender,instance=None,created=False,**kwargs):
    """
    创建用户时自动生成Token
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Token.objects.create(user=instance)


@csrf_exempt
def course_list(request):
    """Django原生FBV式编写API"""
    if request.method == 'GET':
        return JsonResponse(course_list)

    if request.method == 'POST':
        course = json.loads(request.body.decode('utf-8'))
        return JsonResponse(course,safe=False)

@method_decorator(csrf_exempt,name='dispatch')
class CourseList(View):
    """Django原生CBV式编写API"""
    def get(self,request):
        return JsonResponse(course_list)

    # @csrf_exempt 可以在类函数头上加，也可以加在类名上，注意是装饰dispatch
    def post(self,request):
        course = json.loads(request.body.decode('utf-8'))
        return JsonResponse(course, safe=False)

@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication,TokenAuthentication]) # 为视图绑定验证方式，会禁用全局设置
def course_list_api(request):
    """DRF用FBV式编写API"""
    if request.method == 'GET':
        s = CourseSerializer(instance=models.Course.objects.all(),many=True)
        return Response(data=s.data,status=status.HTTP_200_OK)

    if request.method == 'POST':
        s = CourseSerializer(data=request.data) # 如要部分更新（需设置字段可为空）则加上partial=True
        if s.is_valid():
            s.save(teacher=request.user)
            return Response(data=s.data,status=status.HTTP_201_CREATED)
        return Response(data=s.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE','PATCH'])
def course_detail_api(request,pk):
    try:
        course = models.Course.objects.get(pk=pk)
    except models.Course.DoesNotExist:
        return Response(data={"msg":"没有此课程"},status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == 'GET':
            s = CourseSerializer(instance=course)
            return Response(data=s.data,status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            s = CourseSerializer(instance=course,data=request.data)
            if s.is_valid():
                s.save()
                return Response(data=s.data,status=status.HTTP_200_OK)
            return Response(data=s.errors,status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PATCH':
            s = CourseSerializer(instance=course,data=request.data)
            if s.is_valid():
                s.save()
                return Response(data=s.data,status=status.HTTP_200_OK)
            return Response(data=s.errors,status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CourseListAPI(APIView):
    """DRF用CBV开发API"""
    def get(self,request):
        query_set = models.Course.objects.all()
        s = CourseSerializer(instance=query_set,many=True)
        return Response(data=s.data,status=status.HTTP_200_OK)

    def post(self,request):
        s = CourseSerializer(data=request.data) # 如要部分更新（需设置字段可为空）则加上partial=True
        if s.is_valid():
            s.save(teacher=self.request.user)
            return Response(data=s.data,status=status.HTTP_201_CREATED)
        return Response(data=s.errors,status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPI(APIView):
    @staticmethod
    def get_course(pk):
        """
        返回访问的数据
        :param pk: 想要访问的数据的主键
        :return: 数据对象
        """
        try:
            return models.Course.objects.get(pk=pk)
        except models.Course.DoesNotExist:
            return

    def get(self,request,pk):
        course = self.get_course(pk=pk)
        if course is None:
            return Response(data={"msg":"课程不存在"},status=status.HTTP_404_NOT_FOUND)
        s = CourseSerializer(instance=course)
        return Response(data=s.data, status=status.HTTP_200_OK)
    def put(self,request,pk):
        course = self.get_course(pk)
        if course is None:
            return Response(data={"msg":"课程不存在"},status=status.HTTP_404_NOT_FOUND)
        s = CourseSerializer(instance=course,data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data,status=status.HTTP_200_OK)
        return Response(data=s.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        course = self.get_course(pk)
        if course is None:
            return Response(data={"msg":"课程不存在"},status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""通用类模型视图GCBV,推荐！！"""
class GCourseListAPI(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    # 因为要添加教师，所以需重写添加方法，可以点进ListCreateAPIView里看到
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class GCourseDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

"""DRF的viewsets，比GCBV还简洁，强烈推荐！！！"""
class CourseViewSets(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [BasicAuthentication,TokenAuthentication] # 类视图绑定验证的方法

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
