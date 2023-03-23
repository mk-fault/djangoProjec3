from django.urls import path,include
from drf import views

"""注意！！！使用DRF的viewset的路由注册方法"""
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(prefix="viewset",viewset=views.CourseViewSets)

urlpatterns = [
    # FBV
    path("fbv/list/",views.course_list_api,name='fbv-list'),
    path("fbv/detail/<int:pk>/",views.course_detail_api,name='fbv-detail'),
    path("cbv/list/",views.CourseListAPI.as_view(),name='cbv-list'),
    path("cbv/detail/<int:pk>/",views.CourseDetailAPI.as_view(),name='cbv-detail'),
    path("gcbv/list/",views.GCourseListAPI.as_view(),name='gcbv-list'),
    path("gcbv/detail/<int:pk>/",views.GCourseDetailAPI.as_view(),name='gcbv-detail'),

    # 使用DRF的viewset的路由注册方法
    path("",include(router.urls))
]