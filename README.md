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

# RUNNING THE PROGRAM

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

