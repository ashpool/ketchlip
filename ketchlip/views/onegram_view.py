from ketchlip.views.base_view import BaseView

class OnegramView(BaseView):
    def show(self):
        return \
"""
<html>
{% for e in word_count %}
    <div>{{ e[0] }}: {{ e[1] }}</div>
{% endfor %}
</html>
"""