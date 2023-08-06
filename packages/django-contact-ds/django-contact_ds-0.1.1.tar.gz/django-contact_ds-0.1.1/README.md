django-contact_ds
==========

django-contact_ds is a Django app to use for demiansoft.

Quick start
------------

1. Add "contact" to your INSTALLED_APPS setting like this::
```python
INSTALLED_APPS = [
    ...
    'contact',
    'appointment', # contact 컴포넌트 내부에 appointment가 있는 테마의 경우
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load contact_tags %}
{% make_contact %}
```

3. appointment 의 anchor 설정을 위해서 테마 앱의 views.py 안의 buildup 함수의 POST 설정에서 anchor를 추가한다.
```python
from appointment.templatetags.appointment_tags import make_post_context

...
if request.method == 'GET':
    return render(request, f"mentor_ds/base.html", context)
elif request.method == "POST":
    context.update(make_post_context(request.POST, context['basic_info']['consult_email'], anchor="contact"))
    return render(request, f"mentor_ds/base.html", context)
```

* context example
```python
context = {
        "color": "default",
        "theme": "mentor_ds",
        "naver": "https://booking.naver.com/booking/13/bizes/441781",
        "contact": {
            "desc": "3호선, 8호선 가락시장역 2번출구 잠실방향으로  도보로 2분 거리에 위치",
            "google_map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3165.53885481917!2d127.11330765109818!3d37.49520717971214!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357ca593b8c5f7ef%3A0xc814cf4db2f054ea!2z6rCA65297IK87ISx7LmY6rO87J2Y7JuQ!5e0!3m2!1sko!2skr!4v1648771966798!5m2!1sko!2skr",
            "address": "서울시 송파구 양재대로",
            "phone": "02-431-2804",
            "noti": {
                "title": "Parking",
                "desc": [
                    "가락시장 가락몰 주차장 이용(2시간 주차지원)",
                    "네비게이션 : 서울웨딩타워 검색",
                ]
            },
            "timetable": {
                "title": "진료시간",
                "desc": {
                    "월수금": "09:00 am – 06:00 pm",
                    "화(야간)": "09:00 am – 08:00 pm",
                    "토": "10:00 am – 02:00 pm",
                    "점심시간": "012:30 pm – 01:30 pm"
                },
                "note": [
                    "<span class='text-primary'>목요일</span>은 휴진입니다.",
                    "<span class='text-primary'>토요일</span>은 점심시간 없이 진료합니다.",
                ]
            }
        }
    }
```

* how to embed google map : https://support.google.com/maps/answer/144361?hl=en&co=GENIE.Platform%3DDesktop
