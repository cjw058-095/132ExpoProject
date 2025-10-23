import smtplib
from email.message import EmailMessage
import random
import os

def sendmail(recipient_email):
    # Generate random 6-digit token
    token = str(random.randint(100000, 999999))
    
    # Email credentials
    Bulldog_Locker_Email = "bulldoglocker88@gmail.com"  # Replace with your actual email
    Bulldog_Locker_Email_Password = os.getenv('My_Secret_Password')
    
    # Create email
    em = EmailMessage()
    em['From'] = Bulldog_Locker_Email
    em['To'] = recipient_email
    em['Subject'] = 'Your Verification Code - Shared Locker'
    
    # HTML email body with the bulldog image
    html_body = f'''
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h2 style="color: #2c3e50;">Welcome to Shared Locker!</h2>
            <p style="font-size: 18px;">Your verification code is:</p>
            <h1 style="color: #e74c3c; font-size: 48px; margin: 20px 0;">{token}</h1>
            <img src="https://d2gjqh9j26unp0.cloudfront.net/profilepic/8c3fd397c87a9cb7cb7ec8e3772752e5" 
                 alt="Bulldog Mascot" 
                 width="300"
                 style="margin: 20px 0;">
            <p style="font-size: 16px; color: #555;">Enter this code to access your locker.</p>
            <p style="font-size: 14px; color: #888;">Thank you for using Shared Locker!</p>
        </body>
    </html>
    '''
    
    # Plain text version (fallback for email clients that don't support HTML)
    em.set_content(f'Your verification code is: {token}\n\nEnter this code to access your Shared Locker.')
    
    # Add HTML version
    em.add_alternative(html_body, subtype='html')
    
    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Bulldog_Locker_Email, Bulldog_Locker_Email_Password)
        smtp.sendmail(Bulldog_Locker_Email, recipient_email, em.as_string())
    
    return token