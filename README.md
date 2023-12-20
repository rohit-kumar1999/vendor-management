# Vendor Management System (VMS) App

## Overview
The Vendor Management System (VMS) is a web application built using Django, a high-level Python web framework. This application is designed to streamline and manage purchase orders, vendors and their performance.

## Features

### Performance Tracking: 
Evaluate and track vendor performance over time, enabling data-driven decision-making and fostering better relationships with key suppliers.

### Purchase Order Integration: 
Seamlessly integrate with the purchase order system to streamline the procurement process and ensure accurate and timely orders.


## Installation
Clone the repository:

`git clone https://github.com/rohit-kumar1999/vendor-management.git`

Install dependencies:

`pip install -r requirements.txt`

Navigate to the project directory:

`cd vendorManagement`

Apply database migrations:

`python3 manage.py migrate`


Create a superuser account (for admin access):

`python3 manage.py createsuperuser`

Run the development server:

`python3 manage.py runserver`

Access the application at http://localhost:8000 and log in with the superuser credentials.

## Configuration

### Database Configuration: 
Configure the database settings in the settings.py file.

### Usage
Log in with the superuser account created during installation.
create JWT token with `api/jwt/token` api and refresh it `api/jwt/token/refresh` and pass access token as Bearer in order to use apis
Explore the dashboard and navigate to different sections for vendor management.

Use the admin panel to add/edit vendors, manage orders, performance.
