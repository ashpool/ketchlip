from ketchlip.views.base_view import BaseView

class OnegramView(BaseView):
    def show(self):
        return \
"""
<html>
    <head>
        <title>Ketchlip</title>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([
                ['Word', 'Count']
                {% for e in word_count %},['{{ e[0] }}', {{ e[1] }}]{% endfor %}
            ]);

            var options = {
              title: 'Word Count',
              vAxis: {title: 'Count',  titleTextStyle: {color: 'blue'}}
            };
            var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
    </head>
    <body>
        <div id="chart_div" style="width: 100%; height: 100%;"></div>
    </body>
</html>
"""