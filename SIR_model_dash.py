######################################################################################################################################################################
# MODELLO SIR PER LA DIFFUSIONE DI MALATTIE
######################################################################################################################################################################

# 1 - PACCHETTI
# 2 - STILI
# 3 - BARRA DI NAVIGAZIONE
# 4 - PAGINA HOME
# 5 - PAGINA DOCUMENTAZIONE
# 6 - PAGINA SCENARIO
#       - pannello di controllo
#       - barra dei dettagli a dx
#       - grafico centrale
#       - costruzione della pagina
# 7 - MODELLO MATEMATICO
#       - equazione differenziale del modello SIRS
#       - Soluzione del modello SIRS
#       - Funzione che calcola quanti S0 ho per il callback
#       - Funzione che calcola le percentuali di S,I,R
# 8 - CALLBACKS
# 9 - CREAZIONE OUTPUT
#       - creazione dell'oggetto dashboard
#       - funzione per determinare quale pagina stai guardando
#       - aggiunta del layout e dei callbacks
#       - apertura browser e collegamento

######################################################################################################################################################################
# 1 - PACCHETTI
######################################################################################################################################################################

#dash visualization 
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

#maths
import pandas as pd
import numpy as np
from math import log10, floor
from scipy.integrate import odeint

#deployment
import webbrowser
from threading import Timer

######################################################################################################################################################################
# 2 - STILI
######################################################################################################################################################################

def SIDEBAR_HIDDEN():
    style = {
        "position": "fixed",
        "top": 62.5,
        "left": "-17rem",
        "bottom": 0,
        "width": "17rem",
        "height": "100%",
        "z-index": 1,
        "overflow-x": "hidden",
        "transition": "all 0.5s",
        "padding": "0rem 0rem",
        "background-color": "#f8f9fa",}
    return style



def SIDEBAR_SHOW():
    style = {
    "position": "fixed",
    "top": 62.5,
    "right": 0,
    "bottom": 0,
    "width": "17rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    }
    return style

def CONTENT_SHORT():
    style = {
    #"transition": "margin-left .5s",
    "margin-left": "25rem",
    "margin-right": "18rem",
    "padding": "2rem 1rem",
    #"background-color": "#f8f9fa",
    }
    return style

def CONTENT_LONG():
    style = {
    #"transition": "margin-left .5s",
    "margin-left": "25rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    #"background-color": "#f8f9fa",
    }
    return style
    
    
def style_bar_left():
    style = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    }
    return style


######################################################################################################################################################################
# 3 - BARRA DI NAVIGAZIONE
######################################################################################################################################################################

def Navbar():

    #pulsante donazioni
    donate = html.Div([
            dbc.Button("Donazione", id="open", n_clicks=0, class_name="me-1", color ="warning"),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Donazione")),
                dbc.ModalBody("""L'accesso a questa dashboard è gratuito perchè sono profondamente convinto che la cultura non abbia prezzo.
                Tuttavia, sviluppare e mantenere il codice per garantire un servizio sempre aggiornato è un lavoro importante. 
                Se hai apprezzato questo strumento, considera una donazione per supportarmi."""),
                dbc.ModalFooter(dbc.Button("Paypal", id = "paypal", className="ml-auto",color = "warning", href='https://paypal.me/alessandrorubin1'))
                ],id="modal",is_open=False,size = "lg"),
        ])

    #struttura dei collegamenti ipertestuali
    nav_links = dbc.Nav([dbc.NavItem(dbc.NavLink(),class_name="me-auto",), # add an auto margin        
                    dbc.NavItem(dbc.NavLink("Home", class_name="ms-2", href= "/home")),
                    dbc.NavItem(dbc.NavLink("Documentazione", class_name="ms-2", href ="/documentazione")),
                    dbc.NavItem(dbc.NavLink("Scenario", href = "/scenario")),
                    dbc.NavItem(dbc.NavLink("Github")),
                    donate
                    ],
                    # make sure nav takes up the full width for auto margin to get applied
                    class_name="w-100",)


    # composizione della barra di navigazione
    navbar = dbc.Navbar(dbc.Container([
                # titolo a sinistra
                html.Div(
                    dbc.Row(dbc.Col(dbc.NavbarBrand(id = "title", class_name="ms-2")), align="center", class_name="g-0",),style={"textDecoration": "none"}
                    ),
                # hyper-links di navigazione
                dbc.Row([dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse(nav_links, id="navbar-collapse", is_open=False, navbar=True, ),],
                    class_name="flex-grow-1", ),
            ],fluid=True,),
        dark=True,
        color="dark",)

    return navbar

######################################################################################################################################################################
# 4 - PAGINA HOME
######################################################################################################################################################################
def Home():

    # corpo centrale pagina
    body_home = html.Label("Home Page")
    
    # Creazione della pagina HOME
    home_page = html.Div([ Navbar(),  body_home  ])

    return home_page


######################################################################################################################################################################
# 5 - PAGINA DOCUMENTAZIONE
######################################################################################################################################################################

def Documentazione():

    # corpo centrale pagina
    body_home = html.Label("Documentazione Page")
    
    # Creazione della pagina HOME
    doc_page = html.Div([ Navbar(),  body_home  ])

    return doc_page

######################################################################################################################################################################
# 6 - PAGINA SCENARIO
######################################################################################################################################################################

#=============================================================================================
# PANNELLO DI CONTROLLO 
#=============================================================================================

def Control_Panel():
    
    # ACCORDION ----------------------------------------------------------------------------
    accordion = html.Div(dbc.Accordion([
        
                # Primo ingresso --------------------------------
                dbc.AccordionItem([dbc.Col( children=[

                dbc.Checklist(id="switch",
                                options=[
                                       {"label": "I Rimossi si possono riinfettare", "value": "riinfezioni"}
                                       ],
                                value=[], #values chosen by default, if empty nothing is chosen
                                switch= True #  Set to True to render toggle-like switches instead of checkboxes.
                            )
                                        
                ])], title="Ipotesi del modello" ),
          

                # Secondo Ingresso ---------------------------
                dbc.AccordionItem([dbc.Col( children=[
                    
                    dbc.Row([dbc.Label("Popolazione:", width=7), dbc.Col(dbc.Input(id="popolazione", type="number", value=90000, size="sm"), width=5),],class_name="mb-3",),
    
                    dbc.Row([dbc.Label("Infetti:", width=7),dbc.Col(dbc.Input(id="infetti_iniz", type="number", value=0, size="sm"),width=5),], class_name="mb-3",), 
            
                    dbc.Row([dbc.Label("Rimossi:", width=7), dbc.Col(dbc.Input(id="rimossi_iniz", type="number", value=0, size="sm"),  width=5), ],  class_name="mb-3",),
                                       
                    
                    dbc.Col(dbc.Button(id = "S0",  color="light", class_name="d-grid gap-2 col-12 mx-auto")), 
            
                ])], title="Condizioni demografiche iniziali" ),

                # Terzo Ingresso ------------------------------       
                dbc.AccordionItem([dbc.Col( children=[

                 
                    #infettività
                    dbc.Row([dbc.Label("Infettività:", id = "tooltip_infettività"), 
                            dcc.Slider(min=0, max=100, step=1, value=10, id = "infettività" , marks={0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%'},)],class_name="mb-3",), 
                    #tooltip infettività
                    dbc.Tooltip("L'infettività è la probabilità che un infetto trasmetta la malattia ad un suscettibile incontrandolo.",  target= "tooltip_infettività", placement="right"),
                     
                    #contact rate
                     dbc.Row([dbc.Label("Tasso di contatto:", id = "tooltip_contact_rate",width = 7 ), dbc.Col(dbc.Input(id="contact_rate", type="number", value=5, size="sm"), width = 5)],class_name="mb-3",),
                    #tooltip tasso di contagio
                    dbc.Tooltip("Il tasso di contatto è il numero medio di persone incontrare da una persona ogni giorno. Per ipotesi è supposto costante durante l'epidemia.",  target= "contact_rate", placement="right"),
                    
                    #tasso di contagio
                     dbc.Row([dbc.Label("Virulenza:", id = "tooltip_tasso_contagio"),    dcc.Slider(min=0, max=100, step=1, value=10, id = "contagio" , marks={0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%'},)],class_name="mb-3",),
                                                                            
                    #tooltip tasso di contagio
                    dbc.Tooltip("La virulenza rappresenta la percentuale di Infetti che diventano Rimossi.",  target= "tooltip_tasso_contagio", placement="right"),
                     
                    #tasso di riinfezione
                     html.Div(id = "riinfezione_on/off" , children=[dbc.Row([dbc.Label("Tasso di Riinfezione:", id = "tooltip_tasso_riinfezione"),                                                                 
                            dcc.Slider(min=0, max=1, step=0.1, value=0, id = "riinfezione" , marks={0: '0%', 0.2: '0.2%', 0.4: '0.4%', 0.6: '0.6%', 0.8: '0.8%', 1: '1%'},)],class_name="mb-3",), ]),
                                                                            
                                                                 
                    
                    
                       
                     #tooltip tasso di riinfezione
                    dbc.Tooltip("Il tasso di riinfezione rappresenta la percentuale di Rimossi che ritornano Suscettibili.",  target= "tooltip_tasso_riinfezione", placement="right"),

                ])], title="Caratteristiche del patogeno" ),
                              
    # Chiusura Accordion
    ], start_collapsed = True))
    

    # RESET BUTTON ------------------------------------------------------------
    reset_button = dbc.Row([dbc.Button("Resetta valori",  color="warning", class_name="me-1", href = "http://127.0.0.1:8050/scenario")],  class_name="mb-3",style = {"width": "20rem", "margin": "auto"})


    # TABS --------------------------------------------------------------------
    card_header =  dbc.CardHeader(dbc.Tabs([
                dbc.Tab(label = "Impostazioni", tab_id = "tab_1"),
                dbc.Tab(label = "Trend Temporale", tab_id = "tab_2"),
            ],
            id = "tabs",
            active_tab = "tab_1"),)
    
    card_body = dbc.CardBody( children=[ 

            # tab 1 -----------------------------
            html.Div( id = "tab1-style", children = [accordion]),


            # tab 2 -----------------------------
            html.Div( id = "tab2-style", children = [dbc.Card([                 dbc.CardBody(children = [
                
                     dbc.Row([
                        #input
                        dbc.Label("Seleziona un giorno:", width = 7), dbc.Col(dbc.Input(id="day", type="number", value=0), width =5), ],  class_name="mb-3",),
                    
                        #grafico a torta
                        html.Div(id = "piechart")
                        ]), #-------------chiusura row  
                ]),#---------------chiusura cardbody
        ]), #-------------chiusura card
        
        # reset button into cardbody
        html.P(),
        reset_button,
            
        # chiusura cardbody
        ])
    
    
    return html.Div( dbc.Card([ card_header, card_body]) ,style=style_bar_left())

#=============================================================================================
# BARRA DEI DETTAGLI A DX
#=============================================================================================
def Right_Bar():

    body_style = {"margin": {"b" : 0, "l": 0, "r":0, "t": 0} }
    
    details_card = dbc.Col([
                            html.Div(dbc.Card([dbc.CardBody([html.Div(html.H4("Tasso d'infezione", id = "tooltip_tasso_infezione")), html.Hr() , html.H4(id = "beta"),]),], color="secondary", outline=True), style=body_style),
                            dbc.Tooltip("Il tasso d'infezione è il prodotto tra l'Infettività ed il tasso di contagio. Rappresenta la probabilità media di contagiarsi.",  target= "tooltip_tasso_infezione", placement="right"),
                            html.P(),
                            html.Div(dbc.Card([dbc.CardBody([html.Div(html.H4("Picco Infetti")), html.Hr() ,html.H4(id = "picco"), ]),], color="secondary", outline=True), style=body_style),
                            html.P(),
                            html.Div(dbc.Card([dbc.CardBody([html.Div(html.H4("Durata malattia")), html.Hr() ,html.H4(id = "durata"), ]),], color="secondary" , outline=True), style=body_style),
                            html.P(),
                            html.Div(dbc.Card([dbc.CardBody([html.Div(html.H6("Basic Reproduction Number", id = "basic_reproduction_number")), html.Hr() ,html.H4(id = "brn"),]),], color="secondary", outline = True), style=body_style),
                            dbc.Tooltip("Il Basic Reproduction Number rappresenta il numero medio di persone che un infetto infetta nel tempo in cui è infetto. E' un indice che dipende dal tempo.",  target= "basic_reproduction_number", placement="right"),
                        ], class_name="mb-4", style = body_style) 
    
    right_bar = html.Div(details_card, id="sidebar", style=SIDEBAR_SHOW())

    return right_bar


#=============================================================================================
# GRAFICO CENTRALE 
#=============================================================================================
def central_graph():
       
    graph_scenario = html.Div(dbc.Card([dbc.CardBody([
        
        #Titolo
        dbc.Row([dbc.Col(html.H4("Evoluzione temporale dell'epidemia"), width = 9), 
                        dbc.Col(dbc.Button(" Espandi ", id="button", n_clicks=0, class_name="d-grid gap-2 col-12 mx-auto", color ="warning"),width = 3)
                ]),

        #grafico                         
        html.Hr(), 
        html.Div(id = "scenario_content"),

        #ingresso numero giorni in basso
        html.P(),
        dbc.Row([
            dbc.Col(html.H4(" "), width = 2),
            dbc.Col(html.H4("Asse orizzontale (Giorni):"), width = 6), 
            dbc.Col(dbc.Input(id="giorni", type="number", value=120),width = 3),
            dbc.Col(html.H4(" "), width =1),
                ])                                                                   

        # chiusura graph_scenario                             
        ])], color="secondary", outline=True), id = "pagecontent", style=CONTENT_SHORT())

    return graph_scenario


#=============================================================================================
# COSTRUZIONE DELLA PAGINA
#=============================================================================================
def Scenario():    
    
    scenario_page = html.Div([dcc.Store(id='side_click'),  Navbar(),  Control_Panel(), Right_Bar(), central_graph()])

    return scenario_page




######################################################################################################################################################################
# 7 - MODELLO MATEMATICO
######################################################################################################################################################################

#=============================================================================================
# L'equazione differenziale (discreta) del modello SIRS
#=============================================================================================

# beta: infettività
# P: infettività
# nu: tasso di contagio
# beta = tasso di infezione
# gamma: virulenza
# mu : tasso di riinfezione

def SIRS_model(y, t, N, P, nu, gamma, mu):
    S, I, R = y
    beta = (P/100)*(nu/N)
    gamma = gamma/100 #sto caricando percentuali
    mu = mu/100  #sto caricando percentuali
    dSdt = -beta * S * I + mu*R
    dIdt = beta * S * I  - gamma * I
    dRdt = gamma * I  -mu*R
    return dSdt, dIdt, dRdt

#=============================================================================================
# Soluzione del modello SIRS
#=============================================================================================

def solve_SIR(N, Ndays, I0,R0,P,nu, gamma, mu):
    # Persone suscettibili a inizio pandemia:
    S0 = N - I0 - R0

    # Vettore delle condizioni iniziali
    y0 = S0, I0, R0

    # Partizionamento del periodo in N_t slots
    N_t= Ndays

    #Griglia temporale (in giorni)
    t = np.linspace(0, Ndays, N_t) 

    # Integra il modello SIR sulla griglia di tempo t
    sol = odeint(SIRS_model, y0, t, args=(N,P, nu, gamma, mu))

    return sol


#=============================================================================================
# Funzione che calcola quanti S0 ho per il callback
#=============================================================================================

def S0(N, I0,R0):
    # Persone suscettibili a inizio pandemia:
    S0 = N - I0 - R0
    return f"{S0}"


#=============================================================================================
# Funzione che calcola le percentuali di S,I,R
#=============================================================================================

def percentuali(N,Ndays,I0,R0,P,nu, gamma, mu): 
    # Risolvi il modello SIR 
    sol = solve_SIR(N,Ndays, I0,R0,P,nu,gamma, mu)
    S, I, R = sol.T
    
    dataframe = {"day" : range(len(S)), "S" : list(S) , "I" : list(I) , "R" : list(R)}
    df = pd.DataFrame(data = dataframe)

    return df




######################################################################################################################################################################
# 8 - CALLBACKS
######################################################################################################################################################################

def render_callbacks(app):
    

    # --------------------------------------------------------------------
    # Funzione per cambiare il titolo SIR in base alle ipotesi
    # ---------------------------------------------------------------------   
    def select_title(switch):
        title = "Modello Epidemiologico SIR"
        if "riinfezioni" in switch: #namely, the toggle-switch is selected
            title = title + "S"
        return title
    
    app.callback(Output("title", "children"), [Input("switch", "value")])(select_title)
    
    
    # --------------------------------------------------------------------
    # Funzione per nascondere la barra laterale destra
    # ---------------------------------------------------------------------   
    # La funzione prended il numero di clic del pulsante "espandi"
    # e restituisce lo stile del "contenuto" della dashbord
    
    def toggle_sidebar(n, nclick):
        if n:
            if nclick == "SHOW":
                sidebar_style = SIDEBAR_HIDDEN()
                content_style = CONTENT_LONG()
                cur_nclick = "HIDDEN"
                title = "Più dettagli"
            else:
                sidebar_style = SIDEBAR_SHOW()
                content_style = CONTENT_SHORT()
                cur_nclick = "SHOW"
                title = "Espandi"
        else:
            sidebar_style = SIDEBAR_SHOW()
            content_style = CONTENT_SHORT()
            cur_nclick = 'SHOW'
            title = "Espandi"
            
        return sidebar_style,  cur_nclick,content_style , title
    
    app.callback([Output("sidebar", "style"),
         Output("side_click", "data"),
         Output("pagecontent", "style"),
        Output("button", "children")
         ],
        [Input("button", "n_clicks")],
        [State("side_click", "data")],)(toggle_sidebar)
    
    #==============================================================================================
    ### Apertura modale per la donazione
    #==============================================================================================

    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open

    app.callback(
        Output("modal", "is_open"),
        Input("open", "n_clicks"),
        State("modal", "is_open"),
    )(toggle_modal)



    #==============================================================================================
    ### Funzione per far sparire o ricomparire la barra del tasso di riinfezione
    #==============================================================================================

    def render_slider(switch):
        on = {'display': 'block'}
        off = {'display': 'none'}
        if "riinfezioni" not in switch: #namely, the toggle-switch is non-selected
            return off
        else:
            return on

    app.callback(Output("riinfezione_on/off", "style"), [Input("switch", "value")])(render_slider)
        


    #==============================================================================================
    # Funzione per calcolare S0 nella barra a sinistra
    #==============================================================================================   
    # Funzione che calcola quanti S0 ho per il callback
        
    def S0(N, I0, R0):
        # Persone suscettibili a inizio pandemia:
        S0 = N - I0 - R0
        return f"Suscettibili: {S0}"

    app.callback(
        Output("S0", "children"),
        [Input(component_id='popolazione', component_property='value'),
        Input(component_id='infetti_iniz', component_property='value'),
        Input(component_id='rimossi_iniz', component_property='value'),
        ])(S0)
    

    #==============================================================================================
    # Funzione per calcolare il grafico a torta
    #==============================================================================================   
    
    def generate_chart(N,Ndays,I0,R0, P,nu, gamma, mu,day):
        df = percentuali(N,Ndays,I0,R0, P,nu, gamma, mu)
        df = df[df["day"]== int(day)]
        row = df.values.tolist()[0]
        values = [row[1], row[2], row[3]]
        fig = go.Figure(data=[go.Pie(labels=["Suscettibili", "Infetti", "Rimossi"], values= values , hole=.4, sort = False)])
        fig.update_layout(overwrite=True,
                width = 280,
                height=340,
                margin = {"b" : 0, "l": 0, "r":0, "t": 0},
                font={"size":18},
                legend=dict( orientation="h", yanchor="bottom", y= -0.3, xanchor="center",  x=0.5 , font={"size":13})
                )
        #fig.update(layout_showlegend=False)
        piechart = dcc.Graph(figure = fig)
        return piechart
    
    
    app.callback(
    Output("piechart", "children"), 
     [Input(component_id='popolazione', component_property='value'),
                    Input(component_id='giorni', component_property='value'),
                    Input(component_id='infetti_iniz', component_property='value'),
                    Input(component_id='rimossi_iniz', component_property='value'),
                    Input(component_id='infettività', component_property='value'),
                    Input(component_id='contact_rate', component_property='value'),
                    Input(component_id='contagio', component_property='value'),
                    Input(component_id='riinfezione', component_property='value'),
                    Input(component_id='day', component_property='value')
     ])(generate_chart)
    
    
    #==============================================================================================
    ### Funzione per selezionare l'output delle Tab nel pannello di controllo
    #==============================================================================================

    def render_tab_content(active_tab):
        on = {'display': 'block'}
        off = {'display': 'none'}
        if active_tab == "tab_2":
            return  off, on
        else:
            return  on, off

    app.callback(
        [Output("tab1-style", "style"),Output("tab2-style", "style")],
        [Input("tabs", "active_tab")])(render_tab_content)
    
    #==============================================================================================
    # Funzione che aggiorna SCENARIO in base ai parametri
    #==============================================================================================

    def update_scenario(N,Ndays,I0,R0,P,nu,gamma, mu,day): 
            # Risolvi il modello SIR 
            sol = solve_SIR(N,Ndays, I0,R0, P,nu, gamma, mu)
            S, I, R = sol.T
        
            # Creazione del dataframe dei valori
            df = pd.DataFrame(sol,columns = ["S", "I", "R"])
            df["Giorno"] = range(Ndays)
        
            # Creazione output 1 -----------------------------------------
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Giorno'], y=df['S'], mode='lines',name='Suscettibili',  line=dict(color='royalblue', width=3)))
            fig.add_trace(go.Scatter(x=df['Giorno'], y=df['I'], mode='lines', name='Infetti', line=dict(color='red', width=3)))
            fig.add_trace(go.Scatter(x=df['Giorno'], y=df['R'], mode='lines', name='Rimossi', line=dict(color='green', width=3)))
            fig.add_vline(x=day)
            
            fig.update_layout(overwrite=True,
                plot_bgcolor="#f8f9fa", # set the background colour
                margin = {"b" : 0, "l": 20, "r":20, "t": 0},
                title={'y':0.98, 'x':0.08, 'xanchor': 'left', 'yanchor': 'top'},
                height = 350,
                #xaxis_title='Giorni', 
                yaxis_title='Popolazione', font={"size":18},
                legend=dict( orientation="h", yanchor="bottom", y=1.02, xanchor="right",  x=1 ))
            
            figure_1 = dcc.Graph(figure = fig)   

            #creazione output 2 ---------------------------------------------
            beta = (P/100)*(nu/N)
            #arrotondiamo
            cifra_sign = -int(floor(log10(abs(beta))))
            contact_rate = f"{int(round(beta*(10**cifra_sign),0))} x 10^[{cifra_sign}]"

            #creazione output 3--------------------------------------------
            brn = "Non Definito"           
            if gamma !=0 and day is not None:    
                brn = f"{round(beta*S[day]*100/gamma,2)}"     

            # creazione output 4 -----------------------------------------
            picco = "Non definito"
            giorno = np.amax(np.where(I == np.amax(I))[0])
            if giorno != 0 and I0 !=0:
                picco = f"Giorno {giorno}"
            
            # creazione output 5 -------------------------------------------            
            durata = f"{int(round(100/gamma,0))} Giorni"
            
            return   figure_1, contact_rate, brn, picco, durata


    app.callback( [Output("scenario_content", "children"),
                   Output("beta", "children"),
                   Output("brn", "children"), 
                   Output("picco", "children"),
                  Output("durata", "children")],
                [Input(component_id='popolazione', component_property='value'),
                    Input(component_id='giorni', component_property='value'),
                    Input(component_id='infetti_iniz', component_property='value'),
                    Input(component_id='rimossi_iniz', component_property='value'),
                    Input(component_id='infettività', component_property='value'),
                    Input(component_id='contact_rate', component_property='value'),
                    Input(component_id='contagio', component_property='value'),
                    Input(component_id='riinfezione', component_property='value'),
                    Input(component_id='day', component_property='value')
                ])(update_scenario)
    
    return app


################################################################################################################
# 9 - CREAZIONE OUTPUT
################################################################################################################


#==============================================================================================
# creazione dell'oggetto dashboard
#==============================================================================================

my_theme = [dbc.themes.YETI]
app = Dash(__name__ , external_stylesheets= my_theme)   


#==============================================================================================
# funzione per determinare quale pagina stai guardando
#==============================================================================================

app.layout =  html.Div([
        # the location object is an input object which takes the href of the navbar
        dcc.Location(id = 'url', refresh = False),
        # in this box we show the output of the hyper-links
        html.Div(id = 'page-content')
    ])

def display_page(path):
    if path == "/home":
        return Home()
    elif path == "/scenario":
        return Scenario()
    elif path == "/documentazione":
        return Documentazione()
    else:
        return Home()

app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])(display_page)
    
#==============================================================================================
# aggiunta del layout e dei callbacks
#==============================================================================================

render_callbacks(app)
              

#==============================================================================================
# apertura browser e collegamento
#==============================================================================================

def open_browser():
    webbrowser.open('http://127.0.0.1:8050/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=False, port = 8050)
    
