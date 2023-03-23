from drf.models import Course
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')
    class Meta:
        model = Course
        fields = '__all__'

# serializers.HyperlinkedModelSerializer,可使序列化后的结果带上url超链接
# class CourseSerializer(serializers.HyperlinkedModelSerializer):
#     teacher = serializers.ReadOnlyField(source='teacher.username')
#     class Meta:
#         model = Course
#         # url是默认名字，可在setting.py中REST_FRAMEWORK设置URL_FIELD_NAME使全局生效
#         fields = ['id','url','name','introduction','teacher','price','created_at','update_at']