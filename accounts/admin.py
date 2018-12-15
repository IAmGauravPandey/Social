from django.contrib import admin
from .models import UserProfile,Post,Friend

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('user','user_info','city','phone','website')

    def user_info(self,obj):
        return obj.description

    def get_queryset(self,request):
        queryset=super(UserProfileAdmin,self).get_queryset(request)
        queryset=queryset.order_by('-phone','-user')
        return queryset

class PostAdmin(admin.ModelAdmin):
    list_display=('title','user','image')


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Friend)
admin.site.site_header='Admin'