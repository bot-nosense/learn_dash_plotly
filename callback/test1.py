
# ví dụ về callback cục bộ và callback toàn cục


# All-in-One Component Example of Dash Tutorial Basic Callback
# https://community.plotly.com/t/all-in-one-component-example-of-dash-tutorial-basic-callback/68294













import uuid
from dash import Dash, dcc, html, Input, Output, callback, MATCH


class TextReplicatorAIO(html.Div):  # html.Div will be the parent component

    # this class creates the 'id' property of each dash element that will be used in callbacks
    class CallbackComponentIDs:
        @staticmethod
        def input_text_box(aio_id):
            return {
                'component': 'TextReplicatorAIO',
                'subcomponent': 'input-text-box',
                'aio_id': aio_id
            }

        @staticmethod
        def output_text_display(aio_id):
            return {
                'component': 'TextReplicatorAIO',
                'subcomponent': 'output-text-display',
                'aio_id': aio_id
            }

    # make ids class a public class so that TextReplicatorAIO components can be used in callbacks
    # of other dash components. If aio_id = 'user_id_1' then using a subcomponent in an external
    # callback would look like this Input(TextReplicatorAIO.ids.input_text_box('user_id_1'), 'value')
    ids = CallbackComponentIDs

    def __init__(self, aio_id: str = None, header_text: str = None, initial_value: str = None):
        # user supplied aio_id needs to be unique across all instances, if one is not provided
        # create a random id for them
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # create the parent html.Div element called in the main class declaration
        super().__init__(
            id=f'TextReplicatorAIO-{aio_id}',
            children=[
                html.H3(header_text),
                html.Div([
                    "Input: ",
                    dcc.Input(id=self.CallbackComponentIDs.input_text_box(aio_id),
                              value=initial_value,
                              type='text')
                ]),
                html.Br(),
                html.Div(id=self.CallbackComponentIDs.output_text_display(aio_id)),
            ]
        )

    @staticmethod
    @callback(
        Output(component_id=CallbackComponentIDs.output_text_display(MATCH), component_property='children'),
        Input(component_id=CallbackComponentIDs.input_text_box(MATCH), component_property='value')
    )
    def update_output_div(input_value):
        return f'Output: {input_value}'


app = Dash(__name__)

app.layout = html.Div(
    id='AppLayoutOuterWrapper',
    children=[
        TextReplicatorAIO(aio_id='user_supplied_id',
                          header_text="User Supplied Header!",
                          initial_value='Syncs To Outer'),
        html.Br(),
        TextReplicatorAIO(header_text='A Completely independent instance and random id.',
                          initial_value='No Outer sync'),
        html.Br(),
        html.H2(id='outer-element-for-display')
    ]
)


@app.callback(
    Output('outer-element-for-display', 'children'),
    Input(TextReplicatorAIO.ids.input_text_box('user_supplied_id'), 'value')
)
def update_outer_element(user_input_value):
    return f'Replicated To Outer: {user_input_value}'


if __name__ == '__main__':
    app.run_server(debug=True)