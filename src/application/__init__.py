from flask import Flask, render_template, request, redirect, url_for
from application.Forms import CreateUserForm, CreateCustomerForm
import shelve
from application.Models.User import User
from application.Models.Customer import Customer

app = Flask(__name__)

# CONSTANTS USED BY OUR PAGES
# For stuff like colour schemes.
# Todo

# Includes
from application.Controllers.admin import admin_home


@app.route('/')
@app.route('/home')
def home():
    # render a template
    return render_template('home.html')


@app.route('/contactus')
def contact_us():
    # render a template
    return render_template('contactUs.html')


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        with shelve.open('user.db', 'c') as db:

            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db['Users'] = users_dict
            except:
                print("Error in retrieving Users from user.db.")

            user = User(create_user_form.first_name.data, create_user_form.last_name.data,
                             create_user_form.gender.data, create_user_form.membership.data,
                             create_user_form.remarks.data)
            users_dict[user.get_user_id()] = user
            db['Users'] = users_dict
            db["count"] = User.count_id  # VERY IMPORTANT - Save count ID back

            # Test codes
            # users_dict = db['Users']
            # user = users_dict[user.get_user_id()]
            # print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==",
            #       user.get_user_id())

        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        with shelve.open('customer.db', 'c') as db:

            try:
                customers_dict = db['Customers']
            except:
                print("Error in retrieving Customers from customer.db.")

            customer = Customer(create_customer_form.first_name.data,
                                create_customer_form.last_name.data,
                                create_customer_form.gender.data, create_customer_form.membership.data,
                                create_customer_form.remarks.data, create_customer_form.email.data,
                                create_customer_form.date_joined.data,
                                create_customer_form.address.data, )
            customers_dict[customer.get_customer_id()] = customer
            db['Customers'] = customers_dict
            db["count"] = Customer.count_id

        return redirect(url_for('home'))
    return render_template('createCustomer.html', form=create_customer_form)


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    with shelve.open('user.db', 'r') as db:
        users_dict = db['Users']

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    with shelve.open('customer.db', 'r') as db:
        customers_dict = db['Customers']

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        # TODO: Perform checks for access rights or unique values
        users_dict = {}
        try:
            with  shelve.open('user.db', 'w') as db:
                users_dict = db['Users']

                user = users_dict.get(id)
                user.set_first_name(update_user_form.first_name.data)
                user.set_last_name(update_user_form.last_name.data)
                user.set_gender(update_user_form.gender.data)
                user.set_membership(update_user_form.membership.data)
                user.set_remarks(update_user_form.remarks.data)
                db['Users'] = users_dict
        except:
            print('An error have occurred in Update User POST')

        return redirect(url_for('retrieve_users'))
    else:
        # TODO: perform checks for access rights here
        users_dict = {}
        try:
            with shelve.open('user.db', 'r') as db:
                users_dict = db['Users']
        except:
            print('An error have occurred in Update User GET')

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=update_user_form)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        # TODO: Perform checks for access rights or unique values
        customers_dict = {}
        try:
            with shelve.open('customer.db', 'w') as db:
                customers_dict = db['Customers']

                customer = customers_dict.get(id)
                customer.set_first_name(update_customer_form.first_name.data)
                customer.set_last_name(update_customer_form.last_name.data)
                customer.set_gender(update_customer_form.gender.data)
                customer.set_membership(update_customer_form.membership.data)
                customer.set_remarks(update_customer_form.remarks.data)

                customer.set_date_joined(update_customer_form.date_joined.data)
                customer.set_email(update_customer_form.email.data)
                customer.set_address(update_customer_form.address.data)

                db['Customers'] = customers_dict
        except:
            print(f'An error have occured in update customer POST')

        return redirect(url_for('retrieve_customers'))
    else:
        # TODO: perform checks for access rights here
        customers_dict = {}
        try:
            with shelve.open('customer.db', 'r') as db:
                customers_dict = db['Customers']
        except:
            print('An error have occurred in update customer GET')

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.membership.data = customer.get_membership()
        update_customer_form.remarks.data = customer.get_remarks()

        update_customer_form.email.data = customer.get_email()
        update_customer_form.date_joined.data = customer.get_date_joined()
        update_customer_form.address.data = customer.get_address()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        with shelve.open('user.db', 'w') as db:
            users_dict = db['Users']
            if id in users_dict:
                users_dict.pop(id)
            db['Users'] = users_dict
    except Exception as e:
        print(f'An Error have occurred in delete_user({id}) - {e}')

    return redirect(url_for('retrieve_users'))


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    try:
        with shelve.open('customer.db', 'w') as db:
            customers_dict = db['Customers']
            if id in customers_dict:
                customers_dict.pop(id)
            db['Customers'] = customers_dict
    except Exception as e:
        print(f'An Error have occurred in delete_customer({id}) - {e}')

    return redirect(url_for('retrieve_customers'))


with app.app_context():  # run before doing anything else; a la main() -ash
    # Get current customer and admin ID count to prevent overriding
    with shelve.open("customer.db", 'c') as db:
        if "count" in db:
            print("Found customer count in db: %d" % db["count"])
            Customer.count_id = db["count"]
        else:
            print("Initializing customer count in db")
            db["count"] = Customer.count_id  # initialize it:

    with shelve.open("user.db", 'c') as db:
        if "count" in db:
            print("Found user count in db: %d" % db["count"])
            User.count_id = db["count"]
        else:
            print("Initializing user count in db")
            db["count"] = User.count_id  # initialize it:

    app.run()



if __name__ == '__main__':
    app.run()
