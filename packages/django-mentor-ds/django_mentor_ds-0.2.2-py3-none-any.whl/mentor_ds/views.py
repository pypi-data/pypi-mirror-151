from django.shortcuts import render
from appointment.templatetags.appointment_tags import make_post_context
from _data import context

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def buildup(request):
    c = context.context
    # django-base-ds에 아래 코드가 이미 포함되어 있음. 링크만 추가하면됨
    # <link rel="preconnect" href="https://fonts.googleapis.com">
    # <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    c['font_link'] = "https://fonts.googleapis.com/css2?" \
                     "family=Dongle:wght@300;400;700&" \
                     "family=Black+Han+Sans&" \
                     "family=Noto+Sans+KR:wght@100;300;400;500;700;900&" \
                     "family=Noto+Serif+KR:wght@200;300;400;500;600;700;900&display=swap"
    logger.debug(c)
    if request.method == 'GET':
        return render(request, f"mentor_ds/base.html", c)
    elif request.method == "POST":
        # appointment가 contact에 포함된 경우는 anchor를 contact으로 설정한다.
        c.update(make_post_context(request.POST, c['basic_info']['consult_email'], anchor='contact'))
        return render(request, f"mentor_ds/base.html", c)
