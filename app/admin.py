from django.contrib import admin
from app.models.customer import M_Customer
from app.models.confi import M_List_of_Values
from app.models.user import M_User
from app.models.roles import M_Menu,M_Role,M_Role_Menu_Mapping,M_Sub_Menu 
# Register your models here.
admin.site.register(M_Customer)
admin.site.register(M_Role)
admin.site.register(M_Menu)
admin.site.register(M_Sub_Menu)
admin.site.register(M_Role_Menu_Mapping)
admin.site.register(M_List_of_Values)

admin.site.register(M_User)
