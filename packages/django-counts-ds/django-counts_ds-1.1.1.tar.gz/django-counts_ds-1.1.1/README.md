django-counts_ds
==========

django-counts_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "counts" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'counts',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load counts_tags %}
{% make_counts %}
```

* context example
```python
# 문자열을 | 으로 나누면 medicio 템플릿에서 나눠서 사용한다.
context = {
    "theme": "mentor_ds",
    "counts": [
        ["fa-map-pin", "누적 임플란트 식립|임플란트는 어떻게", 17862, "#link"],
        ["fa-thumbs-up", "누적 교정 케이스|교정은 어떻게", 3345, "#link"],
        ["fa-user-md", "의료진", 3, "#link"],
        ["fa-tooth", "누적 사랑니 발치", 16678, "#link"]
    ],
}
```

* Required vendor - purecounter