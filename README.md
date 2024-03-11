WareHouses Project

This project is necessary for the production of products in the production enterprise
about the available raw materials (is there enough raw materials in the warehouse,
how much is there, how much is missing, and how much from which batch
receiving) sending a request to the warehouse for information

Commands for running this project

 -- pip install -r requirements.txt
 -- python manage.py migrate
 -- python manage.py createsuperuser
 
Enter user and password , confirm password
Add information from the admin to the database

After

 -- python manage.py runserver
 
Enter Postman for test
To this url : http://127.0.0.1:8000/warehouse/

For example:
   method POST:
          product_id : 1
          quantity : 30
          product_id : 2
          quantity : 30
