from ketchlip.views.base_view import BaseView

class SearchView(BaseView):
    def show(self):
        return  \
"""
<!DOCTYPE html>
<html>
    <head>
        <title>Ketchlip</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link href="/images/favicon.ico" rel="icon" type="image/x-icon" />
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <link href="/styles/ketchlip.css" rel="stylesheet" type="text/css"/>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
    </head>
    <body>
        <div class="content">
            <img src="/images/logo.png"/>
            <form autocomplete="off">
                <input id="status" type="text" name="search" value="{{query}}"/>
                <button>Search</button>
            </form>
        </div>

        <div><p>{{results_len}} results ({{'%.2f' % search_time_in_ms}} ms)</p></div>

        {% for result in results %}
            <div class="result">
                <div><a class="title" href="{{ result[0] }}">{{ result[2] }}</a></div>
                <div class="url">{{ result[1] }}</div>
                <div class="description">{{ result[3] }}</div>
            </div>
        {% endfor %}
    </body>


    <script>
        $(document).ready(function() {
            $("button").button();
        });
        $(document).ready(function() {
            $('input[type="text"]').addClass("idleField");

            $('input[type="text"]').focus(function() {
                $(this).removeClass("idleField").addClass("focusField");
                this.select();
            });


            $('input[type="text"]').blur(function() {
                $(this).removeClass("focusField").addClass("idleField");
            });

            $('input[type="text"]').focus();

        });
    </script>
</html>
"""

