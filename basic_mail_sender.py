import smtplib
import ssl

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Forgot password</h1>
            <div>
                <form action="/forgot_password" method="post">
                    <label for="email">Enter Email: </label></br>
                    <input type="text" id="email" name="email"></br>
                    <input type="submit" value="Send Verification Passcode">
                </form>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=HTMLResponse)
async def display_page():
    return generate_html_response()


@app.post("/forgot_password")
async def send_mail(email: str = Form(...)):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "enter-sender-mail"
    receiver_email = email
    password = "your-password"
    message = """\
    Subject: Account Recovery
    
    Your passcode is : 123456."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return {"mail sent to": receiver_email,
            "successful": "is successful"
            }
