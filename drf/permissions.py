from rest_framework import permissions
class IsOwnerEditOnly(permissions.BasePermission):
    """自定义权限，仅允许课程所有者修改课程信息"""
    def has_object_permission(self, request, view, obj):
        """
        重写此方法就能自定义对象的权限控制
        :param request:
        :param view:
        :param obj:需要自定义权限控制的类对象（示例为GCourseDetailAPI):
        :return: True表示可以访问，当request为SAFE_METHODS以外的访问时校验当前的user和课程的teacher
        """
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS = ['GET','HEAD','OPTIONS']
            return True

        return request.user == obj.teacher