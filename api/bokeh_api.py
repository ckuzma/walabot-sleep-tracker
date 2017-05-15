from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

class BokehAPI:
    def __init__(self):
        self.plot = None

    def _create_plot(self, title, x_label, y_label):
        self.plot = figure(title=title, x_axis_label=x_label, y_axis_label=y_label)

    def _add_line(self, x_vals, y_vals, label, color='blue', width=0.25):
        self.plot.line(x_vals, y_vals, legend=label, line_width=width, line_color=color)

    def _get_html(self, page_title='Blank'):
        return file_html(self.plot, CDN, page_title)

    def make_graph(self, title, x_lab, y_lab, lines):
        """
        Accepts in a list of objects, each one following this format:
        {
            'x_vals': [],
            'y_vals': [],
            'color': 'blue'
        }
        Returns a string consisting of HTML data. (The graph.)
        """
        self._create_plot(title, x_lab, y_lab)
        for line in lines:
            self._add_line(line['x_vals'], line['y_vals'], '', width=2, color=line['color'])
        return self._get_html()

if __name__ == '__main__':
    # Instantiate the class
    bokeh = BokehAPI()

    # Test data
    lines = [{
            'x_vals': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'y_vals': [0, 0, 5, 3, 3, 3, 5, 5, 0, 0, 0],
            'color': 'blue'
    }]
    graph_title = 'test'
    x_label = 'x values'
    y_label = 'y values'

    # Graph the data
    graph_html = bokeh.make_graph(graph_title, x_label, y_label, lines)

    # Print out the result
    print(graph_html)
