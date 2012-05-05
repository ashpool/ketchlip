from ketchlip.views.base_view import BaseView

class OnegramView(BaseView):
    def show(self):
        return \
"""
<!DOCTYPE html>
<html>
    <head>
        <title>Ketchlip</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link href="/images/favicon.ico" rel="icon" type="image/x-icon" />
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <link href="/styles/ketchlip.css" rel="stylesheet" type="text/css"/>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([
                ['Word', 'Count']
                {% for e in top_100 %},['{{ e[0] }}', {{ e[1] }}]{% endfor %}
            ]);

            var options = {
              title: 'Top 100',
              vAxis: {title: 'Count',  titleTextStyle: {color: 'blue'}}
            };
            var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
    </head>
    <body>
        <div id="chart_div" style="width: 1000px; height: 500px;"></div>
        <div>Words: {{ number_of_words }}</div>
        <div>Pages: {{ number_of_pages }}</div>
        <div>Loaded: {{ load_time }}</div>
    </body>
</html>
"""