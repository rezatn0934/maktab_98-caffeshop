# Caffe Shop Django Project
Welcome to the Caffe Shop Django project! 

## Table of Contents
* [About the Project](#about-the-project)
* [Build With](#build-with)
* [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)

* [Running the Project](#running-the-project)
* [License](#license)
* [Contributing](#contributing)



## About the Project
This project is a web application built with Django framework for managing a coffee shop's orders and sales. This README file will guide you through the setup process, provide instructions for running the project, and explain how to contribute to its development.


## Build With
* [![Django][django.js]][django-url]
* [![JavaScript][JavaScript.js]][JavaScript-url]
* [![HTML][HTML.js]][HTML-url]
* [![CSS][CSS.js]][CSS-url]


## Setup
<a name="Prerequisites"></a>
### Prerequisites
Before setting up the Caffe Shop Django project, ensure that you have the following prerequisites installed on your machine:
- [![Python][Python.js]][Python-url]
- [![PIP][PIP.js]][PIP-url]
- [![Github][Github.js]][Github-url]


### Installation
Follow these steps to set up the project:

Clone the repository using Git:

```
git clone https://github.com/rezatn0934/maktab_98-caffeshop.git

```
Change into the project directory:
```
cd maktab_98-caffeshop
```
Create a virtual environment (optional but recommended):
```
python3 -m venv env
```

Activate the virtual environment:

For Windows:

```
env\Scripts\activate
```
For macOS/Linux:

```
source env/bin/activate
```
Install the project dependencies:

```
pip install -r requirements.txt
```
This command will install all the required Python packages listed in the requirements.txt file.

Set up the database:

```
python manage.py migrate
```
This will apply the database migrations and create the necessary tables.

Create a superuser account (admin):

```
python manage.py createsuperuser
```
Follow the prompts to set a username and password for the admin account.

Congratulations! The Caffe Shop Django project has been successfully set up on your machine.


### Running the Project
To run the Caffe Shop Django project, follow these steps:

Activate the virtual environment (if not already activated):

For Windows:

```
env\Scripts\activate
```
For macOS/Linux:

```
source env/bin/activate
```
Start the server:

```
python manage.py runserver
```
Open your web browser and navigate to http://localhost:8000/. You should see the Caffe Shop web application.

To access the admin interface, go to http://localhost:8000/admin and log in using the superuser account created earlier.

That's it! You can now explore and interact with the Caffe Shop Django project.

a>
### License
![MIT][MIT.js]


### Contributing
We welcome contributions to the Caffe Shop Django project. If you'd like to contribute, please follow these steps:

Fork the repository on GitHub.

Clone your forked repository to your local machine:

```
git clone https://github.com/your-username/maktab_98-caffeshop.git
```
Create a new branch for your changes:


```
git checkout -b feature/your-feature-name
```
Make the necessary changes and commit them:


```
git commit -m "Add your commit message here"
```
Push your changes to your forked repository:

```
git push origin feature/your-feature-name
```
Open a pull request on the original repository, describing your changes and explaining why they should be merged.

Wait for the project maintainers to review your pull request. Once approved, your changes will be merged into the main project.

Thank you for your interest in contributing to the Caffe Shop Django project! We appreciate your help.

[django.js]: https://img.shields.io/badge/Django-F77FBE?style=for-the-badge&logo=django&logoColor=black
[django-url]: https://www.djangoproject.com/
[JavaScript.js]: https://img.shields.io/badge/JavaScript-A21441?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://www.javascript.com/
[HTML.js]: https://img.shields.io/badge/HTML-00A693?style=for-the-badge&logo=html5&logoColor=black
[HTML-url]: https://www.javascript.com/
[CSS.js]: https://img.shields.io/badge/CSS-32127a?&style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://www.javascript.com/
[Python.js]: https://img.shields.io/badge/Python-red?style=for-the-badge&logo=python&logoColor=black
[Python-url]: https://www.python.org/
[PIP.js]: https://img.shields.io/badge/PIP_(Python_package_manager)-blue?style=for-the-badge&logo=pypi&logoColor=white

[PIP-url]: https://pypi.org/
[Github.js]: https://img.shields.io/badge/GitHub-green?style=for-the-badge&logo=github&logoColor=black
[Github-url]: https://github.com/
[MIT.js]: https://img.shields.io/badge/License-MIT-F77FBE.svg
[MIT-url]: https://www.python.org/
