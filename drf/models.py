from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=64,unique=True,verbose_name='课程名称',help_text='课程名称')
    introduction = models.TextField(verbose_name='课程介绍',help_text='课程介绍')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='课程讲师',help_text='课程讲师')
    price = models.DecimalField(max_digits=6,decimal_places=2,help_text='课程价格',verbose_name='课程价格')
    creat_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name
        ordering = ('price',)

    def __str__(self):
        return self.name



