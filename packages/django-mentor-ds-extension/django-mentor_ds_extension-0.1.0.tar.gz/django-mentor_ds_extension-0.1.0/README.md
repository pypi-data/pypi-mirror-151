django-mentor_ds_extension
==========

django-mentor_ds는 mentor_ds 템플릿의 확장형으로 언어선택지원과 1인강사지원의 추가기능을 넣었다.

Quick start
------------

1. 본 템플릿은 다음의 필수 앱들이 필요하다. 프로젝트의 settings.py에 다음을 추가한다.
```python
INSTALLED_APPS = [
    ...
    
    'django.contrib.humanize',
    
    'mentor_ds',
    
    # 필수 컴포넌트
    'popup',
    'base',
    'hero',
    
    # 선택 공통 컴포넌트
    'counts',
    'about',
    'whyus',
    'testimonials',
    'team',
    'faq',
    'contact',
    'appointment',  # contact에서 내부적으로 사용함
    
    # 선택 유니크 컴포넌트
    'courses',
    'features',
    'events',
    'pricing',
    
    # 확장 컴포넌트
    'lang',
    'intro',
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
    path('', include('mentor_ds.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

4. BASE_DIR에 _data폴더를 생성하고 context.py를 생성한다.

5. BASE_DIR에 _static폴더를 생성하고 이미지를 저장한다.

* 프레임으로 창을 띄울때 거부하는 문제 해결위해 settings.py에 다음을 주석처리함.
```python
MIDDLEWARE = [
    ...
    # 프레임으로 창을 띄울때 접속을 거부하는 문제 해결
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

* context는 context_eng, context_kor 두가지 버전으로 준비하여 언어를 선택할 수 있도록 한다.

* context에 추가될 언어설정 및 intro 예시
```python
context = {
    'components' : [
        ...
        ['intro', True, 'Teacher', True],
    ]
    'lang': {
        'list': ['eng', 'kor'],
        'selected': 'eng'
    },
    'intro': {
        'heading': "해외 여행, 비즈니스 업무, 언어 능력 시험, 이민 준비 등 영어와 관련된 목표가 있으신가요? 이러한 목표를 달성하기 위해, 영어로 생각하고 표현할 수 있는 능력을 지속적으로 향상시켜줄 코치가 필요합니다.",
        "desc": "저는 학생들의 스피킹 실력이 향상되고 자신감을 가질 뿐만 아니라 일상에서 영어를 사용하며 즐거워하는 것을 보면서 큰 보람을 느꼈습니다. 많은 분들이 이 즐거움을 저와 함께 느꼈으면 좋겠습니다. 언제든지 편하게 연락주세요!",
    }
}
```
