Introduction

This application sends personalized discount emails to the subscribed user based on the current weather of user’s location.


Tech Stack

- Django REST framework as backend
- ReactJS as frontend

-----------------------------------------------------------------------------------------------
Installation

requirements - python 2.7, pip, npm

Django-rest
- Under folder klaviyo_weather_backend is the Django backend
- cd to klaviyo_weather_backend
- pip install -r requirements.txt
- python manage.py runserver

ReactJS
- Under folder klaviyo_weather_ui is the ReactJS frontend
- cd to klaviyo_weather_ui
- npm install to install dependencies
- npm start
-----------------------------------------------------------------------------------------------

System Design

- As a best practice, the UI layer is kept away from the backend. If in future the code can be extended to mobile apps and for integration with other systems. The REST API can be used to develop on top of it.

- Django rest framework is used in the backend for all the CRUD and DB interactions

- As mentioned in the specification Wunderground API has been used to get the details of the current weather and historical data to come up with the personalized message for the users

- The current timezone of the user based on location is fetched from Wunderground API and stored as part of the db model to improve performance. This field is widely used to send of email based on timezone

- For email notification SendGrid has been used. SendGrid provides python API interface to send out emails

- Each of the modules has been separated out and exposed as  REST API. Details of APIs is listed below in   the API documentation section


-----------------------------------------------------------------------------------------------

How it is Designed ?

Security

- Validations are taken care in the frontend and in the backend to handle proper user input

- The Django emailField is used in the backend to validate all the invalid email inputs and the http response code of the REST API is used to validate the frontend forms

- In the future, each user can have a separate personalized page and should be give privileged to select the discount notification he/she has to receive

Re-Usability

- As I mentioned earlier, most of the components of the app is exposed as a REST API. User subscription, cities, messages, send email are the components which can be re-used by other sections of the code anytime.

Re-Inventing the Wheel?

- As mentioned earlier, in the security sections, instead of build a email validation system from the scratch the best way is to use the existing ones. I have used the django's default emailField which takes care of the validations

- For sending email, I have used SendGrid. The pain of configuring the SMTP server is taken care by SendGrid. I just used the API from SendGrid to send out emails.

Usability

- The app by default is simple and provides easy-of-use. Just in matter of time the user can subscription to location

- To improve the current app, instead of having a list of values for selecting locations, a map can be displayed, so it will be easier for the user to visualize straight away

-----------------------------------------------------------------------------------------------

Email Script

- klaviyo_weather_backend/emailScript.py has the code for email Script
- This python script uses the exposed API to send email to the user
- The script has provision to send out emails based on timezone
- This script can be executed in a cron job to send out emails every morning at 7 AM for each location by based on timezone of the user

- The cron job can run every morning multiple time in one hour interval for each of the timezone so that all the timezones are covered.

-----------------------------------------------------------------------------------------------
Db model

- City
    - id
    - name
    - state
    - population
    - growth

- User
  - email
  - cityId - fk
  - timezone
  - creationTime

-----------------------------------------------------------------------------------------------
REST API Documentation

- http://<hostname:port>/klaviyo-weather/api/users

  Methods
    - POST - This method is for registering user with the System

      Payload
      {
        "email": "test@example.com",
        "cityId": "1"
      }

- http://<hostname:port>/klaviyo-weather/api/cities

  Methods
    - GET - Return the list of available cities available in the System
    Sample Response
    {
        "id": 1,
        "name": "New York",
        "state": "New York"
    }

- http://<hostname:port>/klaviyo-weather/api/messages?cityId=<id>

  Methods
  - GET - Returns the personalized message with city and weather information
    Sample Response
    {
      "city": "Los Angeles",
      "state": "California",
      "subject": "It's nice out! Enjoy a discount on us.",
      "body": "89.0 degree, Clear",
      "icon_url": "http://icons.wxug.com/i/c/k/clear.gif",
      "avg": "71.5"
    }

- http://<hostname:port>/klaviyo-weather/api/sendEmail
  Methods
  - POST - Sends personalized email to the user of the system based on the subscription
  payload
   - If POST is done without any payload then email is sent to all the users of the System. Should
     be very careful with this.

   - If a timezone is passed a payload then the users subscribed to the cities falling the timezone
     will get notified

    {
      "timezone":"PDT"
    }
