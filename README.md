# Setup

You need to have the following installed to be able to use the code
1. MongoDB
2. Virtualenv


### MongoDB 

Database name is DVDRentals

Collection name is films and customers 

## Installation
Create virtual environment and activate

```bash
   virtualenv venv -p python3
   source venv/bin/activate
```

Install the dependencies
```bash
pip install -r requirements.txt
```

Run the web app
```bash
python web.py
```

### API endpoints

- All customers - ```/api/customers```
- Movies customer rented - ```/api/customers/<customer_id>```
- All films - ```/api/films```
- Customers who rented a film - ```/api/customers/films/<film_id>```

### Tables to illustrate can be access via browser
These tables data is loaded via JSON using jquery

- All customers - ```http://127.0.0.1:5000/customers```
- Customer rentals ```http://127.0.0.1:5000/customer_rentals```
- Film details with list of customers who rented it ```http://127.0.0.1:5000/film_customer_rentals``` 


### Here along with API , frontend is also implemented