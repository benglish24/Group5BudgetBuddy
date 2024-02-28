# BudgetBuddy
Budget Buddy functions as a daily budget tracking program that takes 
a user's requested budget and creates a daily budget based on how 
much a user would like to spend in a week.

# Contributors
- Anne-Marie Cobb
- Braxton English
- Cameron Matherne
- Lance Hargrave
- Kevin Nguyen

# Running the application 

To get the application running on your machine, you might need to install
depenencies on both the backend and the frontend. I will go back and 
edit this file once I make sure that this is the proper way to go about 
dealing with installing depenencies (not sure if this is 100% best practice
since I had to use --force but it got the application running).

To install frontend dependencies, make sure that you are in the frontend 
directory, (cd frontend) then you can install dependencies through npm 
in the terminal via command: npm install (I had to do npm install --force)

To install backend dependencies, open a new terminal and switch to the
backend diretory (cd ../backend), then install dependencies through npm 
by command: pip install -r requirements.txt

Once dependencies are installed, the frontend and backend can both be 
started from their respectable directories with the following commands:
frontend: npm run dev
backend: py manage.py runserver

# Setting up a virtual environment

Since its recommended due to a lot of installs from a requirement.txt file, its better to develop this project
in a virtual enviroment. The way to do it is super easy.

Here is a link for the visual info on how to do this:
https://docs.google.com/presentation/d/1IeM7DCn6KfYXFCM6s_eN9Za1A3zlviLm/edit?usp=sharing&ouid=114585968962595015184&rtpof=true&sd=true

Instructions:
1. Install python(preferabbly the most recent version)
2. Install git bash(this is my preferred method of using linux based commands on windows but you can use CMD for instance)
3. Once installed, the project repo should have a virtual enviroment made, start the virtual enviroment based on these commands:
    source venv/bin/activate       # Linux and Mac bash shell
    source venv/Scripts/activate   # Windows bash shell
    .\venv\Scripts\activate        # Windows CMD or powershell

4. I am not sure if VS code will be installed automatically, but it should be.
5. In your commandline, you can use code . to open VSCode and will open the repo of the project
6. If you instead wish to use command line, these are the commands you need to use
    python manage.py collectstatic  #collects static files, run this if you are hitting errors or when first opening the project
    python manage.py makemigrations 
    python manage.py migrate        #shouldn't need to be use unless you create a new model, but its incase you hit errors just run these 2 migration commands
    python manage.py runserver      #This runs the server, should take you to the login page that is setup. 
        - If you need, the link to the local server when running is: 127.0.0.1:8000/