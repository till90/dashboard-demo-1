import dash
from dash import Dash, html
from apps import navigation
import dash_bootstrap_components as dbc

dash.register_page(__name__,path='/info',title="Info",description="Information about different parameters",image='logo2.png')

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Accordion([
                    dbc.AccordionItem(
                        [
                            html.P("Der Oberrheingraben ist ein Lehrbuchbeispiel für ein kontinentales Rift. Er stellt den zentralen Teil eines seit ca. 40 Millionen Jahren bestehenden, tektonischen Bruchsystems dar, das sich quer durch Europa verfolgen lässt. Der Oberrheingraben hat sich dabei über mehrere Kilometer abgesenkt. Gleichzeitig wurde der Graben im Laufe der Zeit durch Eintrag von Grabenrändern, Meeren und Flüssen mit Sediment verfüllt. Seit ca. 20 Millionen Jahren kommt es durch den Druck der Alpen neben der Absenkung des Oberrheingrabens auch zu einer horizontalen Verschiebung. So haben sich die Gebiete östlich des Oberrheingrabens gegenüber den westlichen um etwa 18 km nach Norden verschoben. Die Häufung von Erdbeben im Bereich des Oberrheingrabens belegt, dass das Bruchsystem auch heute noch aktiv ist."),
                            dbc.Button("Click here"),
                        ],
                        title = "Oberrheingraben"
                    ),
                    dbc.AccordionItem(
                        [
                            html.P("Genau durch Darmstadt verläuft die östliche Hauptrandverwerfung des Oberrheingrabens. Große Teile des westlichen Stadtgebietes von Darmstadt werden von geologisch jungen Sedimenten des Oberrheingrabens aufgebaut. Östlich der Verwerfung dagegen liegen mehrere 100 Millionen Jahre alte Kristallingesteine, die geologisch gesehen dem Odenwald zugerechnet werden. Im Detail besteht die Verwerfung aus mehreren Teilabschnitten unterschiedlicher Orientierung. Der Verwerfungsverlauf ist auch morphologisch an Geländeanstiegen erkennbar, wie zum Beispiel am Staatstheater zu sehen ist. "),
                            dbc.Button("Click here"),
                        ],
                        title = "Darmstadt"
                    ),
                    dbc.AccordionItem(
                        [
                            html.P("Das darmstadtium liegt an einer geologisch sehr inte­ressanten Stelle, direkt über der östlichen Hauptrandverwerfung des Oberrheingrabens. Damit steht ein Teil des Gebäudes auf dem festen Kristallingestein des Odenwaldes, der andere Teil auf den weichen Sedimenten des Oberrheingrabens. Dies stellte besondere Anforderungen an die Bauplanung und Statik um Gebäudeschäden durch unterschiedliche Setzung zu vermeiden. Die Fundamentplatte im Bereich des Oberrheingrabens wurde daher auf Pfählen gegründet."),
                            dbc.Button("Click here"),
                        ],
                        title = "Darmstadtium"
                    ),
                ]
                    
                ), 
                title="Geologie"
            ),
            dbc.AccordionItem(
                [
                    html.P("This is the content of the second section"),
                    dbc.Button("Don't click me!", color="danger"),
                ],
                title="Parameter",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Parameter",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Ergebnisse",
            ),
        ],
    )
)

layout = html.Div(
    [
        navigation.navbar,
        accordion
    ]
)

