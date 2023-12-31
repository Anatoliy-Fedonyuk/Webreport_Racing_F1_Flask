# This Project: WebReport Racing F1 Flask REST API


### Package "WebReport Racing F1 Flask" - this software package is an open source product and is distributed free of charge. Our project is developing and based on the reports of Monaco Racing 2018 with a full-fledged REST API technology.
#### This project received new functionality for the REST API version through the use of modern SQLite3 databases and ORM technologies, namely the flask_sqlalchemy application for working with them. This application is built with REST API technology and fully wraps the API for our Report Monaco Racing 2018 web application. 
#### Added the ability for the user to receive a server response in two formats of the most common files in the Internet industry to choose from: these are json and xml.
#### Keeping the full functionality of the Web Report, our application has a full-fledged module for testing API functions using UnitTest. And a full version swagger web documentation for users! Where they can test all the paths and options of our application parameters and see the correct server feedback there!


#### In turn our web application a designed in a modern dark style with CSS that calculates and compiles the Monaco 2018 F1 driver's report based on the results of their races. The initial data is taken from the input files. As a check, caching of two endpoints separately using Redis loaded into Docker-Compose has been added.
#### The application was written using the Flask framework and the Jinja template engine. The kit comes with 16 automated "pytest" tests using @pytest.fixture, catching sys.stdout, using the BeautifulSoup scraping library and the built-in regex module.
#### As a result, using the coverage report, the coverage of the application modules with tests was checked and the requirements.txt file was created with a list of all application dependencies!
