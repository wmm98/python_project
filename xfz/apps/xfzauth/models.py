from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


# 重新定义object
class UserManager(BaseUserManager):
    # 创建普通用户，只能内部调用
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError("请传入手机好吗")
        if not username:
            raise ValueError("请传入用户名")
        if not password:
            raise ValueError("请传入密码")
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    # 创建普通用户
    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    # 创建超级用户
    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 不使用默认增长的主键
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_join = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "telephone"
    # 命令行创建用户提示： telephone username password
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = "email"

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username