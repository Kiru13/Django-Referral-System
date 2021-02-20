# A Referral system using Django and Django Rest Framework

* A user can signup and generate their own referral code.
* A user can share their referral code with others via email
* If the other user accepts and signs up using the same referral code, 100 credits will be given to both the users.

## Fork or Clone

* Fork this project or clone it to access all related files
* You can refer -  https://help.github.com/en/github/getting-started-with-github/fork-a-repo
* For cloning

```python
git clone <>
cd referral
```

## Installation

For windows

```python
python -m venv venv
venv/Scripts/activate
```

For Linux

```python
python -m venv venv
source venv/bin/activate
```

Install requirements

```python
pip install -r requirements.txt
```

## Setup

* Add Environment variables
  ```python
    SECRET_KEY = <Django unique secret key>
    DEBUG = <Mode of environment default:True>
    NAME = <postgres database name default:referralDB>
    USER = <postgres database user default:postgres>
    PASSWORD = <postgres database user password default:password>
    HOST = <postgres database server hostname default:localhost>
    PORT = <postgres database server port default:5432>
    EMAIL_FROM = <Host email address>
    EMAIL_PASSWORD = <Host password>
  ```
  Note: Verify above environment variables are set properly and accessible to project
* Database setup
  ```python
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```

## API's usage

### Sign Up API - Signing up user and generate referral code

* API End Point - {server DNS}/referral/signup/ - (POST)
  
  Request Body
   ```python
   {
    "email":"abc@gmail.com",
    "password":"password",
    "referral_code":"referral_code"
  }
    ```



### Share Referral Code API - Share the referral code to given email id 
* API End Point - {server DNS}/referral/share/ - (POST)
  
  Request Body
   ```python
   {
    "referrer":"user_id",
    "to_email":"xyz@gmail.com"
  }
    ```
  
### User Detail API - Get the user detail by userid to get the points earned in total and referral code
* API End Point - {server DNS}/referral/users/{user_id} - (GET)

Note : server DNS - server url such as localhost:8000