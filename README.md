# How To use the application:
- go to the project's root directory (where the manage.py file is)
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver


# Example requests to all endpoints (and all request methods) were performed in postman and file postman.json can be
# imported in postman to test them.

# Filtering list of products is done by adding ?attribute=value and ordering is done by adding ?ordering=attribute
# for ascending ordering or ?ordering=-attribute for descending ordering

# Application uses BasicAuth so the Authorization header requires a value "Basic value" where the value is the encoded
# username and password
# Postman can handle the conversion for us and you can just provide username and password

# To add a product, instead of using json format as in all other endpoints, i used form-data to pass in a picture directly.
# There is an example in the postman.json file

# Endpoints and possible methods:
- /statistics ['GET'] - get a list of top-selling products
- /products/ ['GET','POST'] - get a list of all products or add a new product
- /productCategories/ ['GET','POST'] - get a list of all categories or add a new category
- /orders/ ['GET','POST'] - get a list of all orders or add a new order
- /products/<str:pk> ['GET','PUT','DELETE'] - get, edit, or delete product with passed id
- /productCategories/<str:pk> ['GET','PUT','DELETE'] - get, edit, or delete category with passed id
- /orders/<int:pk> ['GET','PUT','DELETE'] - get, edit, or delete order with passed id

# Users as well as sellers are predefined by the super user (created with python manage.py createsuperuser)
# and can be created through the admin panel (localhost:8000/admin)
# Normal users have role=user and sellers have role=seller
# Anyone can perform GET request, only sellers can perform all PUT, DELETE and POST requests (except for ordering),
# and users can perform orders POST request.

#Accounts i used to test (username, password):
# admin, admin - superuser without role
# user, user - user with the role of user
# seller, seller - user with the role of seller

# Django Rest Framework provides a basic preview of API data when visiting the link from a web browser. Also,
# when creating a request without any data, the response tells what data was not provided in the request body.