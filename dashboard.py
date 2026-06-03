from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import requests
import sqlite3
import pandas as pd
import logging
import smtplib
from email.mime.text import MIMEText
import ssl

app = Dash(__name__, suppress_callback_exceptions=True)  # Enable suppress_callback_exceptions

logging.basicConfig(level=logging.DEBUG)

# Email configuration
EMAIL_ADDRESS = 'hostelnop@gmail.com'  # Your email address
EMAIL_PASSWORD = 'rsvc wxoe rtks sfqa'  # Your email password
TO_EMAIL_ADDRESS = 'ty2roa+nvwmdu2d5n28@sharklasers.com'  # Recipient's email address
SMTP_SERVER = 'smtp.gmail.com'  # Your SMTP server
SMTP_PORT = 465  # Your SMTP port (use 465 for SSL, 587 for TLS)

def send_email_alert(ddos_percentage):
    subject = "DDoS Alert: High DDoS Traffic Detected"
    body = (
        f"Alert: The DDoS traffic has reached {ddos_percentage:.2f}% of the normal traffic volume. "
        f"Please take necessary actions.\n\n"
        f"Recommended actions to mitigate the DDoS attack:\n"
        f"1. Increase monitoring and logging to capture more detailed traffic data.\n"
        f"2. Implement rate limiting to reduce the impact of attack traffic.\n"
        f"3. Deploy DDoS protection solutions such as web application firewalls (WAF) or cloud-based DDoS mitigation services.\n"
        f"4. Update security policies and firewall rules to block malicious IP addresses.\n"
        f"5. Notify the network security team to take further actions."
    )

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL_ADDRESS

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL_ADDRESS, msg.as_string())
            logging.info("Email alert sent successfully")
            return True
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")
        return False

app.layout = html.Div([
    html.H1("DDoS Detection Dashboard", style={
        'textAlign': 'center', 
        'marginBottom': '20px', 
        'color': '#2c3e50', 
        'font-family': 'Arial, sans-serif',
        'font-size': '32px'
    }),
    
    # Instructions Box
    html.Div(
        children=[
            html.H3("Instructions:", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold', 'color': '#2c3e50'}),
            html.Ol([
                html.Li("Enter values in all seven input fields: Fwd Seg Size Avg, Flow IAT Min, Flow Duration, Tot Fwd Pkts, Pkt Size Avg, Src Port, and Init Bwd Win Byts."),
                html.Li("Click the 'Submit' button to get the prediction for the entered data. The prediction will indicate whether the traffic is benign or part of a DDoS attack."),
                html.Li("Use the 'Dashboard Overview' dropdown menu to navigate between different sections of the dashboard:", style={'marginTop': '10px'}),
                html.Ul([
                    html.Li("Benign vs DDoS Graph: Visual representation of the number of benign and DDoS attacks."),
                    html.Li("Feature Information: Detailed explanation of the input features used for prediction."),
                    html.Li("Analysis and Recommendations: Analysis of the traffic data and recommended actions for mitigating DDoS attacks."),
                    html.Li("Prediction Data Table: Displays a table with the prediction data including feature values and their respective predictions."),
                ]),
                html.Li("Review the 'Alert Message' section for any high DDoS traffic alerts and actions to be taken."),
                html.Li("If a high DDoS traffic alert is triggered, an email will be sent to the configured email address."),
                html.Li("Check the 'Email Status' section for confirmation of email alerts."),
            ]),
        ],
        style={
            'backgroundColor': '#f9f9f9', 
            'padding': '20px', 
            'border': '1px solid #ccc', 
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'marginBottom': '20px'
        }
    ),
    
    html.Div([
        html.Div([
            dcc.Input(id='input-1', type='number', placeholder="Fwd Seg Size Avg", style={'marginRight': '10px', 'marginBottom': '10px'}),
            dcc.Input(id='input-2', type='number', placeholder="Flow IAT Min", style={'marginRight': '10px', 'marginBottom': '10px'}),
            dcc.Input(id='input-3', type='number', placeholder="Flow Duration", style={'marginRight': '10px', 'marginBottom': '10px'}),
            dcc.Input(id='input-4', type='number', placeholder="Tot Fwd Pkts", style={'marginRight': '10px', 'marginBottom': '10px'}),
            dcc.Input(id='input-5', type='number', placeholder="Pkt Size Avg", style={'marginRight': '10px', 'marginBottom': '10px'}),
            dcc.Input(id='input-6', type='number', placeholder="Src Port", style={'marginRight': '10px', 'marginBottom': '10px'}),
            dcc.Input(id='input-7', type='number', placeholder="Init Bwd Win Byts", style={'marginBottom': '10px'}),
        ], style={'textAlign': 'center', 'marginBottom': '10px'}),
        
        html.Button('Submit', id='submit-val', n_clicks=0, style={
            'backgroundColor': '#3498db', 
            'color': 'white', 
            'border': 'none', 
            'padding': '10px 20px', 
            'fontSize': '14px', 
            'borderRadius': '5px',
            'cursor': 'pointer',
            'marginBottom': '10px'
        }),
        
        html.Div('Enter values and press submit', id='output-container-button', style={
            'textAlign': 'center',
            'fontSize': '18px',
            'color': '#2c3e50',
            'marginBottom': '20px'
        }),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Dropdown Heading and Menu
    html.H2("Dashboard Overview", style={'textAlign': 'center', 'marginTop': '20px', 'color': '#2c3e50', 'font-family': 'Arial, sans-serif'}),
    dcc.Dropdown(
        id='section-dropdown',
        options=[
            {'label': 'Benign vs DDoS Graph', 'value': 'graph'},
            {'label': 'Feature Information', 'value': 'feature-info'},
            {'label': 'Analysis and Recommendations', 'value': 'analysis'},
            {'label': 'Prediction Data Table', 'value': 'table'}
        ],
        value='graph',
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}
    ),
    html.Div(id='content')
])

@app.callback(
    Output('content', 'children'),
    Input('section-dropdown', 'value')
)
def display_section(value):
    if value == 'graph':
        return html.Div([
            dcc.Graph(id='prediction-graph'),
            html.Div(id='alert-message', style={'padding': '20px', 'borderTop': '1px solid #ccc', 'color': 'red', 'fontWeight': 'bold'}),
            html.Div(id='email-status', style={'padding': '20px', 'borderTop': '1px solid #ccc', 'color': 'green', 'fontWeight': 'bold'}),
        ])
    elif value == 'feature-info':
        return html.Div(id='feature-info', style={'padding': '20px', 'borderTop': '1px solid #ccc'})
    elif value == 'analysis':
        return html.Div([
            html.H4("Analysis and Recommendations", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold', 'color': '#2c3e50'}),
            html.P("If the DDoS traffic is 20–50% of its normal traffic volume, consider taking the following actions:"),
            html.Ul([
                html.Li("Increase monitoring and logging to capture more detailed traffic data."),
                html.Li("Implement rate limiting to reduce the impact of attack traffic."),
                html.Li("Deploy DDoS protection solutions such as web application firewalls (WAF) or cloud-based DDoS mitigation services."),
                html.Li("Update security policies and firewall rules to block malicious IP addresses."),
                html.Li("Notify the network security team to take further actions."),
            ])
        ])
    elif value == 'table':
        return html.Div([
            html.H3("Prediction Data Table", style={'marginTop': '30px', 'textAlign': 'center', 'color': '#2c3e50'}),
            html.Div(id='table-container')
        ])

@app.callback(
    Output('output-container-button', 'children'),
    Input('submit-val', 'n_clicks'),
    [State(f'input-{i}', 'value') for i in range(1, 8)]
)
def update_output(n_clicks, *values):
    if n_clicks > 0:
        if any(value is None for value in values):
            return 'Please fill in all the attributes before submitting.'
        
        data = {
            "Fwd Seg Size Avg": values[0],
            "Flow IAT Min": values[1],
            "Flow Duration": values[2],
            "Tot Fwd Pkts": values[3],
            "Pkt Size Avg": values[4],
            "Src Port": values[5],
            "Init Bwd Win Byts": values[6]
        }
        try:
            response = requests.post('http://127.0.0.1:5000/predict', json=data)
            response.raise_for_status()
            prediction = response.json().get('prediction')
            return f'Prediction: {prediction}'
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return f'Error: {str(e)}'
    return 'Enter values and press submit'

@app.callback(
    [Output('prediction-graph', 'figure'),
    Output('alert-message', 'children'),
    Output('email-status', 'children')],
    Input('submit-val', 'n_clicks')
)
def update_graph_and_alert(n_clicks):
    alert_message = ''
    email_status = ''
    if n_clicks > 0:
        with sqlite3.connect('./predictions.db') as conn:
            df = pd.read_sql_query("SELECT * FROM predictions", conn)
        benign_count = df[df['prediction'] == 'Benign'].shape[0]
        ddos_count = df[df['prediction'] == 'ddos'].shape[0]  # Ensure 'ddos' is correctly spelled and consistent
        
        if benign_count + ddos_count > 0:
            ddos_percentage = ddos_count / (benign_count + ddos_count) * 100
            if ddos_percentage >= 20:
                alert_message = f"Alert: The DDoS traffic has reached {ddos_percentage:.2f}% of the normal traffic volume."
                if send_email_alert(ddos_percentage):
                    email_status = "Email alert sent successfully."
                else:
                    email_status = "Failed to send email alert."
        
        figure = {
            'data': [
                {'x': ['Benign', 'DDoS'], 'y': [benign_count, ddos_count], 'type': 'bar', 'name': 'Benign vs DDoS',
                'marker': {'color': ['green', 'red']}}
            ],
            'layout': {
                'title': 'Prediction Results: Benign vs DDoS',
                'xaxis': {'title': 'Prediction Type'},
                'yaxis': {'title': 'Count'}
            }
        }
        return figure, alert_message, email_status
    return {}, alert_message, email_status

@app.callback(
    Output('feature-info', 'children'),
    Input('section-dropdown', 'value')
)
def update_feature_info(value):
    if value == 'feature-info':
        return html.Div([
            html.H4("Feature Information", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold', 'color': '#2c3e50'}),
            html.Ul([
                html.Li("Fwd Seg Size Avg: The average size of the forward segments."),
                html.Li("Flow IAT Min: The minimum inter-arrival time of the flow."),
                html.Li("Flow Duration: The duration of the flow."),
                html.Li("Tot Fwd Pkts: The total number of forward packets."),
                html.Li("Pkt Size Avg: The average size of packets."),
                html.Li("Src Port: The source port of the traffic."),
                html.Li("Init Bwd Win Byts: The initial backward window bytes.")
            ])
        ])
    return ''

@app.callback(
    Output('table-container', 'children'),
    Input('section-dropdown', 'value')
)
def update_table(value):
    if value == 'table':
        with sqlite3.connect('./predictions.db') as conn:
            df = pd.read_sql_query("SELECT * FROM predictions", conn)
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_header={
                'backgroundColor': '#2c3e50',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'font-family': 'Arial, sans-serif',
                'fontSize': '14px',
                'backgroundColor': '#f2f2f2',
                'color': '#2c3e50'
            }
        )
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)

