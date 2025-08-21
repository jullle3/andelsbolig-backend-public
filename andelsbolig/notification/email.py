from andelsbolig.advertisement.model import Advertisement
from andelsbolig.config.properties import FRONTEND_URL, THUMBNAIL_URL


def generate_email_content(advertisement: Advertisement) -> str:
    """
    Genererer HTML-indhold til e-mailmeddelelsen.

    :param advertisement: Den annonce, der matcher agentens kriterier.
    """
    # Uddrag nødvendige detaljer fra annoncen
    title = advertisement.title or "Ny annonce"
    price = f"{advertisement.price:,} DKK"
    size = f"{advertisement.square_meters} m²"
    address = advertisement.address or "Adresse ikke tilgængelig"
    city = advertisement.city or ""
    ad_link = f"{FRONTEND_URL}/advertisement/{advertisement.id}"

    # HTML-indhold
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            /* Generelle stilarter */
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border: 1px solid #dddddd;
            }}
            .header {{
                background-color: #007BFF;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
            }}
            .content h2 {{
                color: #333333;
                font-size: 20px;
                margin-top: 0;
            }}
            .content p {{
                color: #555555;
                line-height: 1.5;
            }}
            .details {{
                margin: 20px 0;
            }}
            .details table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .details th, .details td {{
                text-align: left;
                padding: 8px;
                border-bottom: 1px solid #dddddd;
            }}
            .details th {{
                background-color: #f9f9f9;
            }}
            .button {{
                text-align: center;
                margin: 20px 0;
            }}
            .button a {{
                background-color: #28A745;
                color: #ffffff;
                padding: 12px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
            }}
            .footer {{
                background-color: #f9f9f9;
                color: #777777;
                padding: 10px;
                text-align: center;
                font-size: 12px;
            }}
            /* Responsive styles */
            @media only screen and (max-width: 600px) {{
                .content {{
                    padding: 10px;
                }}
                .header h1 {{
                    font-size: 20px;
                }}
                .content h2 {{
                    font-size: 18px;
                }}
                .button a {{
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Nyt match fra din bolig agent</h1>
            </div>
            <div class="content">
                <!-- Tilføj hilsen -->
                <p>Kære bruger,</p>
                <p>Vi har fundet en ny annonce, der matcher dine kriterier:</p>
                <h2>{title}</h2>
                <div class="details">
                    <table>
                        <tr>
                            <th>Pris:</th>
                            <td>{price}</td>
                        </tr>
                        <tr>
                            <th>Størrelse:</th>
                            <td>{size}</td>
                        </tr>
                        <tr>
                            <th>Adresse:</th>
                            <td>{address}, {city}</td>
                        </tr>
                    </table>
                </div>
                <div class="button">
                    <a href="{ad_link}">Se annoncen</a>
                </div>
                <p>Hvis du er interesseret, bedes du besøge annoncen for flere detaljer.</p>
                <p>Med venlig hilsen,<br>Andelsbolig Basen</p>
            </div>
            <div class="footer">
                <p>Denne e-mail blev sendt til dig, fordi du har en aktiv agent på vores platform.</p>
                <p><a href="{FRONTEND_URL}/#profile">Afmeld</a> | <a href="{FRONTEND_URL}">Besøg vores hjemmeside</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content
