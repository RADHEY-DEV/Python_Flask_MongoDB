import logging

from flask import Flask, render_template
from flask import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = "DVDRentals"
app.config['MONGO_URI'] = "mongodb://localhost:27017/DVDRentals"

mongo = PyMongo(app)


@app.route('/customers')
def customers():
    try:
        return render_template('customers.html')
    except:
        logging.error(f"Customer not found")
      

@app.route('/customer_rentals/<customer_id>', methods=['GET'])
def customer_rentals(customer_id):
    try:
        return render_template('customer_rentals.html', customer_id=customer_id)
    except:
        logging.error(f"Customer with the ID {customer_id} not found")
      

@app.route('/film_customer_rentals')
def film_customer_rentals():
    try:
        return render_template('film_customer.html')
    except:
        logging.error(f"film not found")


@app.route('/api/customers', methods=['GET'])
def api_customers():
    customers = mongo.db.customers

    data = []  # Create a list of data we want to expose to the API
   
    try:
        for customer in customers.find():
            data.append({'id': customer['_id'],
                        'first_name': customer['First Name'],
                        'last_name': customer['Last Name'],
                        'phone': customer['Phone'],
                        'address': customer['Address'],
                        'district': customer['District'],
                        'country': customer['Country'],
                        'city': customer['City'],
                        'rentals': customer['Rentals']})

          return jsonify(data)
    except:
        logging.error(f"No customer found")
       

@app.route('/api/customers/<customer_id>', methods=['GET'])
def api_customer(customer_id):
    customer_id = int(customer_id)
    customer = mongo.db.customers.find_one({'_id': customer_id})
    if customer:
        rentals = customer['Rentals']
        # Create a list for the customer rental details
        customer_rentals = []
        for rental in rentals:
            rental_duration = mongo.db.films.find_one({'_id': rental['filmId']})['Rental Duration']
            customer_rentals.append(
                {'rental_date': rental['Rental Date'], 'rental_duration': rental_duration,
                 'rental_cost': rental['Payments'][0]['Amount']})
        data = customer_rentals
    else:
        logging.error(f"User with the ID {customer_id} not found")
        data = "No results"
    return jsonify(data)


@app.route('/api/films', methods=['GET'])
def api_films():
    films = mongo.db.films
    if not film:
        logging.error(f"Film with the ID {film_id} not found")
        data = "No results"
        return jsonify(data)
    data = []  # Create a list of data we want to expose to the API
    for film in films.find():
        data.append({'film': {'title': film['Title'],
                              'category': film['Category'],
                              'description': film['Description'],
                              'rating': film['Rating'],
                              'rental_duration': film['Rental Duration']}})

    return jsonify(data)


@app.route('/api/customers/films/<film_id>', methods=['GET'])
def api_film(film_id):
    """
    API end point to get customers who have rented a specific film
    :param film_id:
    :return: film_details and customer details json
    """
    data = {}
    film_id = int(film_id)

    # Get the film details and add to the data that will be return by API
    film = mongo.db.films.find_one({'_id': film_id})
    if not film:
        logging.error(f"Film with the ID {film_id} not found")
        data = "No results"
        return jsonify(data)
    film_details = []
    film_details.append({'title': film['Title'],
                         'category': film['Category'],
                         'description': film['Description'],
                         'length': film['Length'],
                         'rating': film['Rating'],
                         'rental_duration': film['Rental Duration'],
                         'replacement_cost': film['Replacement Cost'],
                         'special_features': film['Special Features']})
    data['film_details'] = film_details

    # get all customers then match filmId with customers' rental filmId
    customer_rentals = []
    customers = mongo.db.customers
    for customer in customers.find():
        for rental in customer['Rentals']:
            if film_id == rental['filmId']:
                customer_rentals.append({'id': customer['_id'],
                                         'first_name': customer['First Name'],
                                         'last_name': customer['Last Name'],
                                         'phone': customer['Phone'],
                                         'address': customer['Address'],
                                         'district': customer['District'],
                                         'country': customer['Country'],
                                         'city': customer['City']})
    data['customers'] = customer_rentals

    return jsonify(data)


if __name__ == '__main__':
    logging.basicConfig(filename='dvdrentals.log', level=logging.INFO)
    app.run(debug=True)
