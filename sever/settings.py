"""
Django settings for sever project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tdxt@z7z^**z@9)jwv+c+2iu04l=dngegsub-m6shb@kn_0oqe"
DATA_UPLOAD_MAX_NUMBER_FIELD = 1000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*1024
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["cloud.zhuddd.icu", "127.0.0.1", "192.168.1.8"]
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'simpleui',
    "mdeditor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "account",
    "file",
    "upload",
    "download",
    "pay",
    "sharefile"
    # "debug_toolbar"
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'utils.myMiddleware.AuthMiddleware'

]

ROOT_URLCONF = "sever.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "sever.wsgi.application"
ASGI_APPLICATION = 'sever.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
            'NAME': 'clouddisk',  # 数据库名称
            'HOST': '127.0.0.1',  # 数据库地址，本机 ip 地址 127.0.0.1
            'PORT': 3306,  # 端口
            'USER': 'root',  # 数据库用户名
            'PASSWORD': '123456',  # 数据库密码
        }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (
    BASE_DIR / "static",
)
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
X_FRAME_OPTIONS = 'SAMEORIGIN'
# 自定义配置
## 文件目录
STATIC_FILES_DIR = BASE_DIR / "filedata"
STATIC_FILES_DIR_FACE = STATIC_FILES_DIR / "face"
STATIC_FILES_DIR_FILE = STATIC_FILES_DIR / "files"
ICON_DIR = BASE_DIR/"static" / "icon"
LOG_DIR = BASE_DIR.parent / "logs"


FILE_CHECK_LENGTH = 1024  # 文件检查长度

## 解码器目录
FFMPEF_PATH = r"D:\毕业设计\sever\utils\ffmpeg"

## 支付宝配置
ALIPAYSEVER = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
CALLBACK = "cloud.zhuddd.icu/api/pay/callback"
PRIVATEKEY = "MIIEowIBAAKCAQEA6HLk2H2nAAg96dmbdJ8MHvG6mvQUjvxP8MpJebQDK/urV6AXXvtH2cy5zhVpbnjMHjdhuxcTw9BYaiw55ZQrSsMRm3Xk2WgqpuqsbD8op8oOOd4fzqeRldEhgenyeaHhWj05Bb+quNCrLqt/cynShz8k8i2Vf7gSico39P+BH5AsdTbg0fUnmKnEbISRWYw36ot7G12GUXoRj98lbGgLGmIksbLV57nmsNR/I3WWvEoVfRXbGqDU4L1HKOVBcNVgQMYCZRnMWcs9Hn97TC73YOJ7i0R5iOl234YHW5ZblzVT3ynHD+BNGKsAd55//aPZ/gtml5I8cZ/J5JQNGUQrTwIDAQABAoIBAFGpi5xDCJiKTLYLLQIbnjaA1f36If7ZxXvilU2cYEDjeZ6fL5a+0M9DjUNJYnDdH1i+PCduRBNW7rjeMLjnBQ6O2XC0SmHWpqVdbJXa2n2YDsdlseb4F716azso5Xa12GXLfGz4mRG0vW738R6UYtIA7Qnn2c207U5bLK111fcwFAcsJ6LVA57fQtIl/Mie50xKOhRcbuFKZEsxF65aOl6wb8ZTYGxYoj7tnanLtGpeQjbHxjlQ5ONZSmx2fqDBaHf4upe6qlepucpGyMQng9FFctQ9DFol3z1DSPrOU47xGINGZdUkjocST2qI+Qg80Rfv5Wmj0JeR7xaEQQA2tIECgYEA9P7Lkz+/1rgTbrX4mg87D0wueSritjgPFK9x1NTW2WGVi35m/pGPGkKtZeg2mJ8CQwGVj1T76iOB4k6FVwoZA6ngmRyafh/DP8R0Ec9b971x2b8EtCoQqjS5U7068gDaIGa7zMwn5ztsURGJVqWaA8kWDJTL69bLMdJwVSM5mCsCgYEA8uPTkQHKJcguxwVCU6L1t+Hy6FZYQ5UiV4tUjflkRB/coGtM1WH8YciHNAMaXWbm52szedYcIXxRen42KdTbNsUjHVBxwxT7hTlN6c+Lkk8wir2pnZ5VOd0eHGx2pkg0sQUpYmLqWO0Rmp6P363mVKRQSeTI3p8Sbf3/4HkRo20CgYAwVvHN/P8aG7nh10/U/fpWO17UE40mDQuUtkVMjC5UN/fszST/R7MnqE5UVCwpkv48QFzFKiyGdzkScRHIKbrjySoCq+0jw5qfw2Bvfy2TRTLoltMTxVUCcGK8zhKKW3aue/bEIuggrM3jdQVXLlekNZH/K4DM6NWw3+fANLIRfwKBgCXvp4+yc9xK0+OJ0r41aaN6yvG26rpDhMWfoWk7Vom9YDw+BhYd48lyBIv/IBMOi2oBuFyDMImaXS+Anv0RnduEFuPxOJN7p307YgvuuqHzdGV3EhLoM++Btb5CwpVeGby8TaZsRKX3ARThRx9sjdkSgOfJsAX1Wm+LiHeK8VJRAoGBAOjBMZIn7GvLVaDGb1jk0TiDNJV0gcIygNLRsuA5fIsQqNvciTdOIuQRLC3fIo2phhzhsO4YhJyhGQ6RXWL8mjBmcGkRbbKhKz6dBIgMbPuE/Fj2WVST1envTMBNHQWCPtzMIn5AKAUoapgHyUt09/rlQDWzvolEqVocpps1psuh";
ALIPAYPUBLICKEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgXvYmNiExfeBh0eXOwrB0pRdElrz1HIvtfJblQQIXCJekfe/IHkooHOsRpYm+nWN9yAadw43Z8ysq9gv2LUTvqzZNZeFzZSj1weA9heG+CMnpjGgM+iTeHMPZh8yGayP5H3rAL8IxLUoeOTZgxgPwh1i8pD9EkS8QDnr5K8aZoTVBSrB2nt72K7HWAeG3143KWRRD9hh3LYLAM1puynsLudWEGQYr7DUsio81mp6c5FilTz/JFZ8WemFhLVx58IhDlTLyY5umkTdLAGLSER8By3M+1so6ZQpBvCjskiuHJe3rCk8uXQGAsxYxZ7pAUZl/KSmiOeqv5SF2SmTYrGa6wIDAQAB";
APP_ID = "9021000122694907"

##管理界面配置
SIMPLEUI_HOME_PAGE="127.0.0.1/api/pay/admin"
SIMPLEUI_HOME_TITLE = 'Cloud'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ICON = {
    '用户': 'fa-solid fa-user',
    '文件': 'fa-solid fa-file',
    '用户文件': 'fa-solid fa-file',
}
SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单，自定义菜单时建议关闭。
    'system_keep': False,

    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。空列表[] 为全部不显示.
    'menu_display': ['用户账户', '文件管理', '支付', '权限认证'],
    # 首页设置
    'dynamic': False,
    'menus': [
        {
            'name': '用户账户',
            'icon': 'fa fa-user',
            'models': [
                {
                    'name': '用户',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/account/user/',
                    'icon': 'fa fa-user'
                },
                {
                    'name': '用户验证码',
                    'url': '/admin/account/captcha/',
                    'icon': 'fa fa-user'
                },
            ]
        },
        {
            'name': '文件管理',
            'icon': 'fa fa-database',
            'models': [
                {
                    'name': '用户文件',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/file/fileuser/',
                    'icon': 'fa fa-file'
                },
                {
                    'name': '文件',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/file/files/',
                    'icon': 'fa fa-file'
                },
                {
                    'name': '文件分享',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/sharefile/sharelist/',
                    'icon': 'fa fa-share'
                },
            ]
        },
        {
            'name': '支付',
            'icon': 'fa-solid fa-cart-shopping',
            'models': [
                {
                    'name': '订阅',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/pay/menu/',
                    'icon': 'fa-solid fa-cart-shopping'
                },
                {
                    'name': '用户订单',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/pay/userorders/',
                    'icon': 'fa-solid fa-cart-shopping'
                },
            ]
        },
        {
            'app': 'auth',
            'name': '权限认证',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '管理员列表',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '管理员用户组',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                }
            ]
        },

    ]
}
