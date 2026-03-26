# django-ticketing
Ticketing is a web application built with Django and SQLite.

# Run the project
1. Go to the project directory:
```
cd ticketing-project
```  
2. Apply migrations (required after clone/fork):
```
python manage.py migrate
```
3. Run the development server:
```
python manage.py runserver 8090
```
4. Open the app in your browser:
```
http://127.0.0.1:8090/tickets/
```

Notes:  
After cloning or forking the repository, you must run migrations before starting the server.  
The project uses SQLite as the default database, so no additional setup is required.
