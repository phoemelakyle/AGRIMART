from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import mysql.connector
from datetime import datetime

seller_orders_app = Blueprint('seller_orders', __name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "agrimart"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def get_unpaid_orders_data(user_id):
    order_details = []

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)

            query_orders = """
            SELECT OrderID, ProductID, VariationID, Quantity, Total_Amount, Order_Date, Payment_OptionsID, Shipping_Address
            FROM Seller_Order
            WHERE Order_Status = 'waiting for payment' AND SellerID = %s
            """
            cursor.execute(query_orders, (user_id,))
            orders = cursor.fetchall()
            
            for order in orders:
                product_id = order['ProductID']
                variation_id = order['VariationID']

                query_product = """
                SELECT Product_Name, ImageFileName, Shipping_Fee
                FROM Product
                WHERE ProductID = %s
                """
                cursor.execute(query_product, (product_id,))
                product_info = cursor.fetchone()

                query_variation = """
                SELECT Color, Size, Price
                FROM Product_Variation
                WHERE VariationID = %s
                """
                cursor.execute(query_variation, (variation_id,))
                variation_info = cursor.fetchone()

                order_detail = {
                    'ImageFileName': product_info['ImageFileName'],
                    'Product_Name': product_info['Product_Name'],
                    'Shipping_Fee': product_info['Shipping_Fee'],
                    'Color': variation_info['Color'],
                    'Size': variation_info['Size'],
                    'Quantity': order['Quantity'],
                    'OrderID': order['OrderID'],
                    'Price': variation_info['Price'],
                    'Total_Amount': order['Total_Amount'],
                    'Shipping_Address': order['Shipping_Address'],
                }
                order_details.append(order_detail)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return order_details

@seller_orders_app.route('/unpaid_orders', methods=['POST','GET'])
def unpaid_orders():
    user_id = session.get('user_id')
    order_details = get_unpaid_orders_data(user_id)

    order_type = 'unpaid'
    return render_template('seller_orders.html', order_details=order_details, order_type=order_type)

def get_to_ship_orders_data(user_id):
    order_details = []

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)

            query_orders = """
            SELECT OrderID, ProductID, VariationID, Quantity, Total_Amount, Order_Date, Payment_OptionsID, Shipping_Address
            FROM Seller_Order
            WHERE Order_Status = 'pending' AND SellerID = %s
            """
            cursor.execute(query_orders, (user_id,))
            orders = cursor.fetchall()
            
            for order in orders:
                product_id = order['ProductID']
                variation_id = order['VariationID']

                query_product = """
                SELECT Product_Name, ImageFileName, Shipping_Fee
                FROM Product
                WHERE ProductID = %s
                """
                cursor.execute(query_product, (product_id,))
                product_info = cursor.fetchone()

                query_variation = """
                SELECT Color, Size, Price
                FROM Product_Variation
                WHERE VariationID = %s
                """
                cursor.execute(query_variation, (variation_id,))
                variation_info = cursor.fetchone()

                order_detail = {
                    'ImageFileName': product_info['ImageFileName'],
                    'Product_Name': product_info['Product_Name'],
                    'Shipping_Fee': product_info['Shipping_Fee'],
                    'Color': variation_info['Color'],
                    'Size': variation_info['Size'],
                    'Quantity': order['Quantity'],
                    'OrderID': order['OrderID'],
                    'Price': variation_info['Price'],
                    'Total_Amount': order['Total_Amount'],
                    'Shipping_Address': order['Shipping_Address'],
                }
                order_details.append(order_detail)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return order_details

@seller_orders_app.route('/to_ship_orders', methods=['POST','GET'])
def to_ship_orders():
    user_id = session.get('user_id')
    order_details = get_to_ship_orders_data(user_id)

    order_type = 'to_ship'
    return render_template('seller_orders.html', order_details=order_details, order_type=order_type)

@seller_orders_app.route('/shipping_orders', methods=['POST','GET'])
def shipping_orders():
    user_id = session.get('user_id')
    order_details = []  

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)

            query_orders = """
            SELECT OrderID, ProductID, VariationID, Quantity, Total_Amount, Order_Date, Payment_OptionsID, Shipping_Address, Shipping_Date
            FROM Seller_Order
            WHERE Order_Status = 'shipping' AND SellerID = %s
            """
            cursor.execute(query_orders, (user_id,))
            orders = cursor.fetchall()
            
            for order in orders:
                product_id = order['ProductID']
                variation_id = order['VariationID']

                query_product = """
                SELECT Product_Name, ImageFileName, Shipping_Fee
                FROM Product
                WHERE ProductID = %s
                """
                cursor.execute(query_product, (product_id,))
                product_info = cursor.fetchone()

                query_variation = """
                SELECT Color, Size, Price
                FROM Product_Variation
                WHERE VariationID = %s
                """
                cursor.execute(query_variation, (variation_id,))
                variation_info = cursor.fetchone()

                order_detail = {
                    'ImageFileName': product_info['ImageFileName'],
                    'Product_Name': product_info['Product_Name'],
                    'Shipping_Fee': product_info['Shipping_Fee'],
                    'Color': variation_info['Color'],
                    'Size': variation_info['Size'],
                    'Quantity': order['Quantity'],
                    'OrderID': order['OrderID'],
                    'Price': variation_info['Price'],
                    'Total_Amount': order['Total_Amount'],
                    'Shipping_Address': order['Shipping_Address'],
                    'Shipping_Date':order['Shipping_Date'],
                }
                order_details.append(order_detail)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    order_type = 'shipping'  
    return render_template('seller_orders.html', order_details=order_details, order_type=order_type)

@seller_orders_app.route('/delivered_orders', methods=['POST','GET'])
def delivered_orders():
    user_id = session.get('user_id')
    order_details = []  

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)

            query_orders = """
            SELECT OrderID, ProductID, VariationID, Quantity, Total_Amount, Order_Date, Payment_OptionsID, Shipping_Address, Shipping_Date
            FROM Seller_Order
            WHERE Order_Status = 'delivered' AND SellerID = %s
            """
            cursor.execute(query_orders, (user_id,))
            orders = cursor.fetchall()
            
            for order in orders:
                product_id = order['ProductID']
                variation_id = order['VariationID']

                query_product = """
                SELECT Product_Name, ImageFileName, Shipping_Fee
                FROM Product
                WHERE ProductID = %s
                """
                cursor.execute(query_product, (product_id,))
                product_info = cursor.fetchone()

                query_variation = """
                SELECT Color, Size, Price
                FROM Product_Variation
                WHERE VariationID = %s
                """
                cursor.execute(query_variation, (variation_id,))
                variation_info = cursor.fetchone()

                order_detail = {
                    'ImageFileName': product_info['ImageFileName'],
                    'Product_Name': product_info['Product_Name'],
                    'Shipping_Fee': product_info['Shipping_Fee'],
                    'Color': variation_info['Color'],
                    'Size': variation_info['Size'],
                    'Quantity': order['Quantity'],
                    'OrderID': order['OrderID'],
                    'Price': variation_info['Price'],
                    'Total_Amount': order['Total_Amount'],
                    'Shipping_Address': order['Shipping_Address'],
                    'Shipping_Date': order['Shipping_Date'],
                }
                order_details.append(order_detail)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    order_type = 'delivered'  
    return render_template('seller_orders.html', order_details=order_details, order_type=order_type)

@seller_orders_app.route('/cancelled_orders', methods=['POST','GET'])
def cancelled_orders():
    user_id = session.get('user_id')
    order_details = []  

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)

            query_orders = """
            SELECT OrderID, ProductID, VariationID, Quantity, Total_Amount, Order_Date, Payment_OptionsID, Shipping_Address
            FROM Seller_Order
            WHERE Order_Status = 'cancelled' AND SellerID = %s
            """
            cursor.execute(query_orders, (user_id,))
            orders = cursor.fetchall()
            
            for order in orders:
                product_id = order['ProductID']
                variation_id = order['VariationID']

                query_product = """
                SELECT Product_Name, ImageFileName, Shipping_Fee
                FROM Product
                WHERE ProductID = %s
                """
                cursor.execute(query_product, (product_id,))
                product_info = cursor.fetchone()

                query_variation = """
                SELECT Color, Size, Price
                FROM Product_Variation
                WHERE VariationID = %s
                """
                cursor.execute(query_variation, (variation_id,))
                variation_info = cursor.fetchone()

                order_detail = {
                    'ImageFileName': product_info['ImageFileName'],
                    'Product_Name': product_info['Product_Name'],
                    'Shipping_Fee': product_info['Shipping_Fee'],
                    'Color': variation_info['Color'],
                    'Size': variation_info['Size'],
                    'Quantity': order['Quantity'],
                    'OrderID': order['OrderID'],
                    'Price': variation_info['Price'],
                    'Total_Amount': order['Total_Amount'],
                    'Shipping_Address': order['Shipping_Address'],
                }
                order_details.append(order_detail)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    order_type = 'cancelled' 
    return render_template('seller_orders.html', order_details=order_details, order_type=order_type)

@seller_orders_app.route('/ship_now/<order_id>', methods=['POST', 'GET'])
def ship_now(order_id):
    user_id = session.get('user_id')
   
    order_details = get_to_ship_orders_data(user_id)

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime('%Y-%m-%d')

            update_query = """
            UPDATE Buyer_Order
            SET Order_Status = 'shipping', Shipping_Date = %s
            WHERE OrderID = %s
            """
            cursor.execute(update_query, (formatted_date, order_id))
            connection.commit()

            update_query = """
            UPDATE Seller_Order
            SET Order_Status = 'shipping', Shipping_Date = %s
            WHERE OrderID = %s
            """
            cursor.execute(update_query, (formatted_date, order_id))
            connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    order_type = 'to_ship'

    return render_template('seller_orders.html', order_details=order_details, order_type=order_type, refresh_page=True)

@seller_orders_app.route('/cancel_unpaid_order/<order_id>', methods=['POST', 'GET'])
def cancel_unpaid_order(order_id):
    user_id = session.get('user_id')
   
    order_details = get_unpaid_orders_data(user_id)

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            update_query = """
            UPDATE Buyer_Order
            SET Order_Status = 'cancelled'
            WHERE OrderID = %s
            """
            cursor.execute(update_query, (order_id,))
            connection.commit()

            update_query = """
            UPDATE Seller_Order
            SET Order_Status = 'cancelled'
            WHERE OrderID = %s
            """
            cursor.execute(update_query, (order_id,))
            connection.commit()

            get_variation_id_query = "SELECT VariationID FROM Seller_Order WHERE OrderID = %s"
            cursor.execute(get_variation_id_query, (order_id,))
            variation_id = cursor.fetchone()[0]

            seller_order_quantity_query = "SELECT Quantity FROM Seller_Order WHERE OrderID = %s"
            cursor.execute(seller_order_quantity_query, (order_id,))
            sl_quantity = cursor.fetchone()[0]
            print(sl_quantity)

            product_variation_quantity_query = "SELECT Quantity FROM Product_Variation WHERE VariationID = %s"
            cursor.execute(product_variation_quantity_query, (variation_id,))       
            pv_quantity = cursor.fetchone()[0]
            print(pv_quantity)

            new_quantity = max(pv_quantity + sl_quantity, 0)
            print(new_quantity)

            update_query = "UPDATE Product_Variation SET Quantity = %s WHERE VariationID = %s"
            cursor.execute(update_query, (new_quantity, variation_id))
            connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    order_type = 'unpaid'

    return redirect(url_for('seller_orders.unpaid_orders'))

@seller_orders_app.route('/cancel_to_ship_order/<order_id>', methods=['POST', 'GET'])
def cancel_to_ship_order(order_id):
    user_id = session.get('user_id')
   
    order_details = get_to_ship_orders_data(user_id)

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            update_query = """
            UPDATE Buyer_Order
            SET Order_Status = 'cancelled'
            WHERE OrderID = %s
            """
            cursor.execute(update_query, (order_id,))
            connection.commit()

            update_query = """
            UPDATE Seller_Order
            SET Order_Status = 'cancelled'
            WHERE OrderID = %s
            """
            cursor.execute(update_query, (order_id,))
            connection.commit()

            get_variation_id_query = "SELECT VariationID FROM Seller_Order WHERE OrderID = %s"
            cursor.execute(get_variation_id_query, (order_id,))
            variation_id = cursor.fetchone()[0]

            seller_order_quantity_query = "SELECT Quantity FROM Seller_Order WHERE OrderID = %s"
            cursor.execute(seller_order_quantity_query, (order_id,))
            sl_quantity = cursor.fetchone()[0]
            print(sl_quantity)

            product_variation_quantity_query = "SELECT Quantity FROM Product_Variation WHERE VariationID = %s"
            cursor.execute(product_variation_quantity_query, (variation_id,))       
            pv_quantity = cursor.fetchone()[0]
            print(pv_quantity)

            new_quantity = max(pv_quantity + sl_quantity, 0)
            print(new_quantity)

            update_query = "UPDATE Product_Variation SET Quantity = %s WHERE VariationID = %s"
            cursor.execute(update_query, (new_quantity, variation_id))
            connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    order_type = 'to_ship'

    return redirect(url_for('seller_orders.to_ship_orders'))