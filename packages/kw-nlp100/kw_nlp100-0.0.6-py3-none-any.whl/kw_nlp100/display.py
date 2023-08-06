import pprint
pp = pprint.PrettyPrinter(width=60, compact=True).pprint

from IPython.display import display, HTML, Markdown
def md(terms):
    terms = terms if (type(terms) == list) else [terms]
    display(Markdown(' / '.join(terms)))

from google.colab import data_table
data_table.enable_dataframe_formatter()

# ちょっとした Hack
# https://stackoverflow.com/questions/59588349/data-table-display-in-google-colab-not-adhering-to-number-formats
data_table._DEFAULT_FORMATTERS[float] = lambda x: f"{x:.3f}"
data_table.disable_dataframe_formatter()

def table(df):
    data_table.enable_dataframe_formatter()
    display(data_table.DataTable(df, num_rows_per_page=10))
    data_table.disable_dataframe_formatter()