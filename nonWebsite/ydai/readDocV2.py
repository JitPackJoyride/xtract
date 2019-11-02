import docx2txt
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import plotly.graph_objs as go
import base64
import os
import io
import pandas as pd
import datetime
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    print(filename)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'doc' in filename:
        # Assume that the user uploaded an excel file
        # df = pd.read_excel(io.BytesIO(decoded))
        print(filename)
        import docx2txt
        my_text = docx2txt.process("doc2.docx")
        print(my_text)
        df = pd.Series(my_text).to_frame("Col")
    # from IPython import embed;
    # embed(header='Debug');
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# def build_body(filename):
#     if filename is not None:
#         my_text = docx2txt.process(filename)
#         print(my_text)
#
#         sentens = my_text.split('\n')
#
#         check1 = [True if ("Sharehold" in x and "Company1" in x) else False for x in sentens]
#         if(any(check1)):
#             body_comps = [html.Div(children="More Document is needed for Company as shareholder: %d" % click)]
#         else:
#             body_comps = [html.Div(children="Everything is good")]
#     else:
#         body_comps = [html.Div(children="Content")]
#     return body_comps
if __name__ == '__main__':
    app.config['suppress_callback_exceptions'] = True  # when components are not available in the initial.
    # app.run_server(debug=True, host='192.168.125.19', port=8080)
    app.run_server(debug=True, host='127.0.0.1', port=8080)