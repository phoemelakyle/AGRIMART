from flask import Blueprint, render_template, request, redirect, session
import mysql.connector
import os
from werkzeug.utils import secure_filename

add_product_app = Blueprint('add_product', __name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "agrimart"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def generate_product_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(ProductID) FROM Product")
    latest_product_id = cursor.fetchone()[0]

    if latest_product_id is not None:
        numeric_part = int(latest_product_id[2:])
        new_numeric_part = numeric_part + 1
    else:
        new_numeric_part = 1000

    product_id = f"PD{new_numeric_part}"
    cursor.close()
    conn.close()

    return product_id  

class Product:
    VOLUMETRIC_FACTOR = 5000
    SHIPPING_RATE_PER_UNIT_WEIGHT = 50
    def __init__(self, productname, weight, packaging_length, packaging_width, packaging_height, category_id, image):
        self.productname = productname
        self.weight = weight
        self.packaging_length = packaging_length
        self.packaging_width = packaging_width
        self.packaging_height = packaging_height
        self.category_id = category_id
        self.image = image
        self.variations = []  
        self.product_id = None

    def add_variation(self, price, quantity, color=None, size=None):
        variation = {'price': price, 'quantity': quantity, 'color': color, 'size': size}
        self.variations.append(variation)

    def generate_variation_id(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(VariationID) FROM Product_Variation")
        latest_variation_id = cursor.fetchone()[0]

        if latest_variation_id is not None:
            numeric_part = int(latest_variation_id[2:])
            new_numeric_part = numeric_part + 1
        else:
            new_numeric_part = 1000

        variation_id = f"VT{new_numeric_part}"
        cursor.close()
        conn.close()

        return variation_id 
    
    def calculate_shipping_fee(self):
        actual_weight = float(self.weight)
        volumetric_weight = (self.packaging_length * self.packaging_width * self.packaging_height) / self.VOLUMETRIC_FACTOR
        return max(actual_weight, volumetric_weight) * self.SHIPPING_RATE_PER_UNIT_WEIGHT

    def insert_into_database(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        product_id = generate_product_id()

        shipping_fee = self.calculate_shipping_fee()

        sql_query = "INSERT INTO Product (ProductID, SellerID, Product_Name, Weight, Packaging_Length, Packaging_Width, Packaging_Height, CategoryID, ImageFilename, Shipping_Fee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (product_id, user_id, self.productname, self.weight, self.packaging_length, self.packaging_width, self.packaging_height, self.category_id, self.image, shipping_fee)

        try:
            cursor.execute(sql_query, values)
            conn.commit()

            
            self.product_id = product_id
            
            for variation in self.variations:
                variation_id = self.generate_variation_id() 
                variation_query = "INSERT INTO Product_Variation (VariationID, ProductID, Color, Size, Price, Quantity) VALUES (%s, %s, %s, %s, %s, %s)"
                variation_values = (variation_id, self.product_id, variation.get('color', None), variation.get('size', None), variation['price'], variation['quantity'])
                cursor.execute(variation_query, variation_values)
                conn.commit()

            return True
        except mysql.connector.Error as e:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

@add_product_app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    from app import app
    user_id = session.get('user_id')
    if 'user_id' not in session:
        session['user_id'] = user_id
    if request.method == 'POST':
        productname = request.form['Product_Name']
        weight = request.form['Weight']
        packaging_length = float(request.form['Packaging_Length'])
        packaging_width = float(request.form['Packaging_Width'])
        packaging_height = float(request.form['Packaging_Height'])
        category_id = request.form['Category']  
        
        image = request.files['Image']
        image_filename = None

        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        if productname and weight and packaging_length and packaging_width and packaging_height and category_id:
            product = Product(productname, weight, packaging_length, packaging_width, packaging_height, category_id, image_filename)

            colors = request.form.getlist('Color')
            sizes = request.form.getlist('Size')
            prices = request.form.getlist('Price')
            quantities = request.form.getlist('Quantity')

          
            for price, quantity, color, size in zip(prices, quantities, colors, sizes,):
                price = float(price) if price else None
                quantity = int(quantity) if quantity else None
                product.add_variation(price, quantity, color, size)

            success = product.insert_into_database(session['user_id'])

            if success:
                return redirect('/add_product')  
            else:
                return redirect('/error')  
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CategoryID, Category_Name FROM Product_Category")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('add_product.html', categories=categories)

@add_product_app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')