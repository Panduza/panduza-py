import pygal
from robot.api import logger
from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of


class KeywordsToolChart(object):

    ###########################################################################
    # DIRECTION
    ###########################################################################

    @keyword
    def create_chart_line(self, title, x_range_list):
        """
        """
        line_chart = pygal.Line()
        line_chart.title = title
        line_chart.x_labels = map(str, x_range_list)
        return line_chart

    @keyword
    def chart_line_add(self, chart_line, name, data):
        """
        """
        chart_line.add(name, data)

    @keyword
    def log_chart(self, chart):
        """
        """
        svg_chart = chart.render()
        logger.write(svg_chart, level='INFO', html=True)

