"""
Django settings for Ecommerce project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'voyxl@1b=ph#1!=1hhu#-a$u-u@!%k4_fllc+=ycq7qtb#r!b#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'goods',
    'users',
    'cart',
    'orders',
    'backmanage',
    'tinymce',
]
CORS_ORIGIN_ALLOW_ALL = True
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.custommiddleware.MiddleWareCus1'
]

ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django03',
        'HOST': '47.102.128.212',
        'USER': 'root',
        'PASSWORD': '1q2w3e',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



# 阿里云短信验证码配置
SMSCONFIG = {
    'ACCESS_KEY_ID': "LTAIwJRC5pKyAD2r",
    'ACCESS_KEY_SECRET': "2bimJuqryCKWQjy6oHLMY6SNyZEK3T",
    'SignName': "歪秀购物",  # 签名
    'TemplateCode': "SMS_169895734"
}

# TINYMCE_DEFAULT_CONFIG = {
#     'theme': 'advanced',
#     'width': 500,
#     'height': 300
# }


TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'width': 500,
    'height': 300
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/upload')
# 允许上传的文件后缀
ALLOWED_FILEEXTS = ['.png', '.jpeg', '.jpg', '.gif', '.bmp']

APP_ID = "2016101100659505"

MERCHANT_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "orders/keys/rsa_private_key.pem")
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "orders/keys/rsa_public_key.pem")


