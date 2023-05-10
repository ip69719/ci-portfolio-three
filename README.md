# Elegant Hairstyles appointments scheduling assistance app

[Link to the live project](https://elegant-hairstyles-booking-app.herokuapp.com/)

## Project Overview

Elegant Hairstyles is a small imaginary hairdressing business that utilises an online appointments scheduling assistance app which runs on Code Institute mock terminal on Heroku.

The app allows customers to view their bookings and to check availablity at any time without the need to contact the Hairdressers.
Staff at Elegant Hairstyles spend less time taking bookings over the phone because customers already know what date and time slot suits them before they call.

![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/image.png)


## Features

### Existing Features

* **Welcome message**
    * Users are greeted with a welcome message which includes a brief description of the app.
    * Users are presented with simple instructions to choosed from.
    ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/welcome.png)

* **Login**
    * Users will be required to enter their email and password to use the app.
    * New users have an option to register.
    ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/login.png)

* **Register**
    * Users will be required to register to use the app.
    * Already registered users can login with their credentials.
    ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/register.png)
    * New user details are added to the [Users](https://docs.google.com/spreadsheets/d/1JK7nrAsio11eWGhl_KE0F8422WZe4lMaXBRTk9-KNjc/edit#gid=32414724) google worksheet.

* **Print Future Appointments**
    * All the upcoming appointments associated with the authenticated user are displayed upon successful login.
    ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/future_appt.png)  

* **Available Appointments**
    * Authenticated users can check if any appointments are available on selected date.
    ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/available_appt.png)  

* Input validation
    * **Email validation**
        * User input for email address is validated against the following pattern: username + @ symbol + domain name.
        * If User enters an invalid email address then the request for data is repeated until an email in a valid format is provided.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/email_validation_error.png)
        * Correctly formatted email is accepted and the registration process progresses to the next step.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/valid_email_reg.png)

    * **Username validation**
        * User input for Username is validated to ensure that it is not empty.
        * If User enters a whitespace character or just hits the return key then the request for data is repeated until expected input is provided.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/username_validation_error.png)
        * Username that meets the requirements is accepted and the registration process progresses to the next step.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/valid_username_reg.png)

    * **Password validation**
        * User input for Password is validated against specified password requirements.
        * Password must be at least eight characters long, must contain at least one digit and must have at least one character in uppercase.
        * If User enters a password which does not meet the requirements then the request for data is repeated until expected input is provided.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/password_validation_error.png)
        * Password that meets the requirements is accepted and the registration process is complete.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/valid_password_reg.png)

    * **Date validation**
        * User input for Date is checked to ensure it matches the expected format and that the date is a future date.
        * If User enters a date which does not meet the requirement then the request for data is repeated until a valid date is provided.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/invalid%20date.png)
        * If date input is valid then user is presented with available appointments for the date selected.
        ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/valid_date.png)

### Features Left to Implement

* Create booking feature was not complete due to time constrains. It will be included in the future release. Code associated with this feature was removed.
* Hide password, so it is not visible when typed in the terminal.
* Reset password.
* Allow stylists check upcoming appointments and client's details via app.

## Technologies used

### Languages used

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Frameworks, Libraries & Programs Used

* [Google Sheets](https://www.google.com/sheets/about/) is used to store data.
* [gspread](https://docs.gspread.org/en/latest/) - a Python API for Google Sheets.
* [google-auth](https://pypi.org/project/google-auth/) is required to set up the authentication needed to access my Google Cloud project.
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html) Python package used to manipulate and display data from Google Sheets.
* [pyglet](https://pypi.org/project/pyglet/) was used to create logo.
* [Tabulate](https://pypi.org/project/tabulate/) Python library used to display Pandas dataframes in a table style.
* [Python Datetime](https://docs.python.org/3/library/datetime.html) module used to manipulate dates.
* [Python Calendar](https://docs.python.org/3/library/calendar.html) module used to get day of the week.
* [Python built-in re package](https://docs.python.org/3/library/re.html) is required for email address validation.
* [Git](https://git-scm.com/) was used for version control by utilising the Gitpod terminal to commit to Git and Push to GitHub.
* [GitHub](https://github.com/) is used to store the project code after being pushed from Git.
* [Heroku](https://www.heroku.com/about) was used to deploy the app. 

## Testing

### Validation Testing

* CI Python Linter was used to validate the code.
    * CI Python Linter - [Results](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/ci_python_linter_results.png): All clear, no errors found.
    ![](https://github.com/ip69719/ci-portfolio-three/blob/main/docs/images/ci_python_linter_results.png)
    * Line too long warnings were ignored because I wanted to center the logo and welcome text on mock terminal on Heroku. In addition, splitting some lines of code resulted in syntax errors. I commented these lines with # noqa:E501 to indicate that the linter should not check these lines.

### Manual Testing

* Test cases are recorded in [this](https://docs.google.com/spreadsheets/d/1qU2jid0vbYUYpUHYSIkKlxukydcZFL5mdR-51esS82A/edit?usp=sharing) shared google workbook.
* Confirmed that User can only enter a valid answer option from the list of available options.
* Confirmed that if invalid answer option is selected, then request for valid input repeated.
* Confirmed that only date provided in expected format (YYYY-MM-DD) is accepted.
* Confirmed that if the input date is not in the future, then request for valid input repeated.
* Confirmed that the same email address cannot register more than once.
* Confirmed that input provided on registration is saved to the user details tab in the spreadsheet.
* Confirmed that appointments associated with the authenticated user only are displayed upon successful login.

### Defect Tracking

Issues are documented and tracked on [GitHub](https://github.com/ip69719/ci-portfolio-three/issues?q=is%3Aissue+is%3Aclosed).

## Version Control
Previously some of my commit messages were too generic. I made improvements in the current release and my commit messages are much more descriptive.

## Deployment

The project was deployed to Heroku using the following steps:

1. Log in to Heroku.
1. Click New in the top right corner and select "Create a new app".
1. Give the app a name and select the closest region, then click 'Create app".
1. Go to "Settings" tab and scroll down to the “Config Vars” section.
    1. click on "Reveal Config Vars".
    1. In the field for key, enter CREDS (connect to API to access Google Sheets spreadsheet).
    1. Copy and paste the entire content of the creds.jason into the value field, then click “Add”.
    1. Configure variable for key PORT and value 8000.
1. In "Settings" tab scroll down to the “Buildpacks” section.
    1. Click on "Add buildpack".
    1. Select "python" and then click "Save changes".
    1. Click on "Add buildpack" again.
    1. Select "nodejs" and then click "Save changes".
1. Go to "Deploy" tab and scroll to the “Deployment method” section.
1. Click on "GitHub".
1. Locate the [GitHub Repository](https://github.com/ip69719/ci-portfolio-three) then click "Connect".
1. In "Deploy" tab scroll down to "Manual deploy" section, select main branch and click on "Deploy Branch"
1. Click "View" to launch the app.

## Credits

### Content

* Content of README.md was written with reference to Code Institute  Portfolio 3 Project Scope.

### Code

* Learned how to connect the API to my spreadsheet, update spreadhseet and deploy the app from Code Institute Love Sandwiches Walkthrough Project.
* Learned about Python exit command from [this](https://pythonguides.com/python-exit-command/#:~:text=In%20python%2C%20we%20have%20an%20in-built%20quit%20%28%29,function%20should%20only%20be%20used%20in%20the%20interpreter.) python tutorial.
* Learned about Python datetime module from [this](https://www.geeksforgeeks.org/formatting-dates-in-python/) GeeksforGeeks tutorial.
* Learned how to get the weekday name from date using calendar module from [this](https://pynative.com/python-get-the-day-of-week/) PYnative tutorial.
* Learned how to read Google Sheets data using Python from [this](https://medium.com/geekculture/2-easy-ways-to-read-google-sheets-data-using-python-9e7ef366c775) article written by BK Lin.
* Learned about ASCII art using pyfiglet module from [this](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/) GeeksforGeeks tutorial.
* Learned how to select rows from Pandas DataFrame based on a condition from [this](https://www.geeksforgeeks.org/how-to-select-rows-from-pandas-dataframe/) GeeksforGeeks tutorial.
* Learned how to validate email address using regular expression from [this](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) GeeksforGeeks tutorial.
* Learned how to trim whitespace from a string in python from [this](https://www.digitalocean.com/community/tutorials/python-trim-string-rstrip-lstrip-strip) Digital Ocean tutorial.
* Learned how to add password checks from [this](https://stackoverflow.com/questions/37794949/regular-expressions-for-password-in-python-3) Stack Overflow post.
* Learned how to display the Pandas DataFrame in table style from [this](https://www.geeksforgeeks.org/display-the-pandas-dataframe-in-table-style/) GeeksforGeeks tutorial.
* Learned how to print Pandas DataFrame without index from [this](https://stackoverflow.com/questions/24644656/how-to-print-pandas-dataframe-without-index) Stack Overflow post.
* Learned how to append rows to empty pandas DataFrame within for Loop from [this](https://statisticsglobe.com/append-rows-pandas-dataframe-loop-python) Statistics Globe tutorial.

### Acknowledgements

* Special thanks to my Mentor [Malia Havlicek](https://github.com/maliahavlicek) for support and guidance during this project.