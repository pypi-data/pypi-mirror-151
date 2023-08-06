django-medilab_ds
==========

django-medilab_ds는 medilab_ds 템플릿의 기본형이다.

Quick start
------------

1. 본 템플릿은 다음의 필수 앱들이 필요하다. 프로젝트의 settings.py에 다음을 추가한다.
```python
INSTALLED_APPS = [
    ...
    
    'django.contrib.humanize',
    
    'medilab_ds',
    
    # 필수 컴포넌트
    'popup',
    'base',
    'hero',
    
    # 선택 공통 컴포넌트
    'about',
    'clients',
    'gallery',
    'cta',
    'services',
    'portfolio',
    'contact',
    'counts',
    'whyus',
    'faq',
    'team',
    'appointment',
    'testimonials',
    
    # 선택 유니크 컴포넌트
    'departments',
]
```

2. static 파일을 저장하기 위해 settings.py에 다음을 추가한다.
```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '_static/'),
]
```

3. 프로젝트의 urls.py에 다음을 추가하여 home app과 템플릿에 연결한다.
```python
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
    path('', include('medilab_ds.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

4. BASE_DIR에 _data폴더를 생성하고 context.py를 생성한다.

5. BASE_DIR에 _static폴더를 생성하고 이미지를 저장한다.

6. 데이터베이스 구성
```commandline
python manage.py makemigrations popup portfolio
python manage.py migrate
```

* 프레임으로 창을 띄울때 거부하는 문제 해결위해 settings.py에 다음을 주석처리함.
```python
MIDDLEWARE = [
    ...
    # 프레임으로 창을 띄울때 접속을 거부하는 문제 해결
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```