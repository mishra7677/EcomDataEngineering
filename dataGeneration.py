from faker import Faker
import pandas as pd
from datetime import date, datetime, timedelta
import random


f=Faker()

# Load data into pandas DataFrame from "/lakehouse/default/" + "Files/import_file/part-00000-63232ee5-dda4-448b-b52d-c0e260bb582e-c000.csv"
product_csvPath="product csv file path"
prodDf = pd.read_csv(product_csvPath)
prodList= prodDf['name'].tolist()

custCartJson="path to your cust cart json file "
custCart=spark.read.format('json').load(custCartJson)
row_list = custCart.collect()
#convert dataframe to list
ccID = [row.asDict() for row in custCart.collect()]



# Generate random customer and cart data
def generate_customer_cart():
    randomElem= f.random_element(elements=ccID)
    custid = randomElem['customerID']
    cartid = randomElem['cartID']
    return {"custid": custid, "cartid": cartid}





class customer:
    
    def __init__(self,custid):
        self.custid = custid
    
    def customerDetails(self):
        customerData={
            'custID':self.custid,
            'Name': f.name(),
            'age': f.random_int(min =16, max= 80),
            'gender': f.passport_gender(),
            'email': f.email(),
            'phoneNumber': f.basic_phone_number()
            }
        
        return customerData
    
    def AddressDetails(self):

        addressData = {
            'custID': self.custid,
            'StreetAddress': f.street_address(),
            'City': f.city(),
            'State': f.state(),
            'ZipCode': f.zipcode(),
            'Country': f.country()
        }
        return addressData

    def membershipDetails(self):
        current_date = datetime.now()
        min_start_date= current_date - timedelta(days= 3650)
        max_end_date = current_date + timedelta(days=365)  # Maximum 12 months from today

        membershipData = {
            'custID': self.custid,
            'MembershipID': f.random_int(min=1, max=999999999),
            'Level': f.random_element(elements=('Silver', 'Gold', 'Platinum')),
            'Start_date': f.date_between(start_date=min_start_date, end_date=current_date),
            'End_date': f.date_between(start_date=current_date, end_date=max_end_date)
        }
        return membershipData



class Product:
    def __init__(self):
        self.productID = f.random_int(min=1, max=999)
    def productDetails(self):
        productData = {
            'ProductID': self.productID,
            'ProductName': f.random_element(elements=prodList),
            'Category': f.random_element(elements=('Electronics', 'Clothing', 'Books', 'Furniture')),
            'Description': f.text()
        }
        return productData

    def productCostHistory(self):
        current_date = datetime.now()
        min_start_date= current_date - timedelta(days= 365)
        max_end_date = current_date + timedelta(days=365) 
        costHistory ={
                'productID': self.productID,
                'startDate':f.date_time_between(start_date=min_start_date, end_date=current_date),
                'endDate':f.date_time_between(start_date=min_start_date, end_date=max_end_date),
                'standardCost': f.random_number(digits=4, fix_len=False)
            }
        return costHistory

    def productLocation(self):
        locationData = {
            'LocationID': f.random_int(min=100, max=999),
            'productid': self.productID,
            'LocationName': f.street_name(),
            'City': f.city(),
            'State': f.state(),
            'Country': f.country()
        }
        return locationData

class cart:
    def __init__(self,cartid):
        self.cartid = cartid
        

    def cartDetails(self,custid):
        self.custid= custid
        
        cart_item = {
            'CartID': self.cartid,
            'ProductID': f.random_int(min=1, max=999),
            'Quantity': f.random_int(min=1, max=10),
            'discount': round(random.uniform(10, 30), 2),
            'customerid': self.custid
        }
        
        
        return cart_item

class shipping:

    def shippingDetails(self):
        current_date = datetime.now()
        min_start_date= current_date - timedelta(days= 365)
        max_end_date = current_date + timedelta(days=365) 
        shipDate=f.date_time_between(start_date=min_start_date, end_date=current_date)
        devlDate= shipDate + timedelta(days=15)
        
        shipping_info = {
            'ShippingID': f.random_int(min=1000, max=9999),
            'ShipmentDate':shipDate,
            'DeliveryDate': f.date_time_between(start_date= shipDate, end_date= devlDate),
            'ShippingAddress': f.street_address(),
            'City': f.city(),
            'State': f.state(),
            'ZipCode': f.zipcode(),
            'Country': f.country()
        }
        return shipping_info

class order:
    def __init__(self,custid,prodID):
            self.customerid= custid        
            self.productid =prodID
    def orderDetails(self):
        current_date = datetime.now()
        min_start_date= current_date - timedelta(days= 3650)
        max_end_date = current_date + timedelta(days=365)
        order_info = {
            'OrderID': f.random_int(min=1, max=9999999999999999999),
            'CustomerID': self.customerid,
            'productID': self.productid,
            'OrderDate':  f.date_time_between(start_date=min_start_date, end_date=current_date),
            'TotalAmount': f.random_int(min=100, max=1000),
            'PaymentMethod': f.random_element(elements=('Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery'))
        }
        return order_info

    def returnOrderDetails(self):
        current_date = datetime.now()
        min_start_date= current_date - timedelta(days= 3650)
        max_end_date = current_date + timedelta(days=365)
        return_order_info = {
            'ReturnID': f.random_int(min=100000, max=999999),
            'OrderID': f.random_int(min=10000, max=99999),
            'customerid':self.customerid ,
            'ReturnReason': f.random_element(elements=('Wrong Item', 'Defective', 'Not as Expected')),
            'ReturnDate': f.date_time_between(start_date=min_start_date, end_date=current_date),
            'RefundAmount': f.random_int(min=50, max=500)
        }
        return return_order_info

    def exchangeOrderDetails(self):
        orderDate=self.orderDetails()['OrderDate']
        exchange_date= orderDate +timedelta(days=30)
        
        exchange_order_info = {
            'ExchangeID': f.random_int(min=1000000, max=9999999),
            'OrderID': f.random_int(min=10000, max=99999),
            'ExchangeReason': f.random_element(elements=('Wrong Size', 'Change of Color', 'Upgrade')),
            'ExchangeDate': f.date_time_between(start_date=orderDate, end_date=exchange_date),
            'ExchangeItem': f.random_element(elements=('Product A', 'Product B', 'Product C'))
        }
        return exchange_order_info

class inventory:
    
    def inventoryDetails(self):
        inventory_info = {
            'ProductID': f.random_int(min=1, max=99999),
            'StockLevel': f.random_int(min=10, max=100),
            'RestockingAlert': f.random_element(elements=('Low Stock', 'Out of Stock', 'Normal')),
            'LastStockUpdate': f.date_this_decade(),
            'SupplierID': f.random_int(min=100, max=999),
        }
        return inventory_info

    def supplierDetails(self):
        supplier_info = {
            'SupplierID': f.random_int(min=100, max=999),
            'SupplierName': f.company(),
            'ContactPerson': f.name(),
            'Email': f.email(),
            'Phone': f.phone_number()
        }
        return supplier_info

    def stockMovementDetails(self):
        stock_movement_info = {
            'ProductID': f.random_int(min=1, max=99999),
            'MovementType': f.random_element(elements=('Sales', 'Returns', 'Restocking')),
            'Quantity': f.random_int(min=1, max=10),
            'MovementDate': f.date_this_decade()
        }
        return stock_movement_info



# Define  classes and methods here (customer, cart, Product, shipping, order, inventory)

# Function to generate data for one hour
def generate_data_for_one_hour():
    # create empty list for each item
    customer_details_list = []
    address_details_list = []
    membership_details_list = []
    product_details_list = []
    product_cost_history_list = []
    product_location_list = []
    cart_details_list = []
    shipping_details_list = []
    order_details_list = []
    return_order_details_list = []
    exchange_order_details_list = []
    inventory_details_list = []
    supplier_details_list = []
    stock_movement_details_list = []

    start_time = datetime.now()
    while datetime.now() - start_time < timedelta(seconds=10):
        # Generate data for each entity
        gcc = generate_customer_cart()
        cart_id = gcc["cartid"]
        customer_id = gcc["custid"]
        cust_obj = customer(customer_id)
        cart_obj = cart(cart_id)
        prod_obj = Product()
        ship_obj = shipping()
        order_obj = order(customer_id, prod_obj.productID)
        inv_obj = inventory()

        # Append data to respective lists
        customer_details_list.append(cust_obj.customerDetails())
        address_details_list.append(cust_obj.AddressDetails())
        membership_details_list.append(cust_obj.membershipDetails())
        product_details_list.append(prod_obj.productDetails())
        product_cost_history_list.append(prod_obj.productCostHistory())
        product_location_list.append(prod_obj.productLocation())
        cart_details_list.append(cart_obj.cartDetails(cust_obj.custid))
        shipping_details_list.append(ship_obj.shippingDetails())
        order_details_list.append(order_obj.orderDetails())
        return_order_details_list.append(order_obj.returnOrderDetails())
        exchange_order_details_list.append(order_obj.exchangeOrderDetails())
        inventory_details_list.append(inv_obj.inventoryDetails())
        supplier_details_list.append(inv_obj.supplierDetails())
        stock_movement_details_list.append(inv_obj.stockMovementDetails())

    data_dict = {
        'customer_df': customer_details_list,
        'address_df': address_details_list,
        'membership_df': membership_details_list,
        'product_df': product_details_list,
        'product_cost_df': product_cost_history_list,
        'product_location_df': product_location_list,
        'cart_df': cart_details_list,
        'shipping_df': shipping_details_list,
        'order_df': order_details_list,
        'return_order_df': return_order_details_list,
        'exchange_order_df': exchange_order_details_list,
        'inventory_df': inventory_details_list,
        'supplier_df': supplier_details_list,
        'stock_movement_df': stock_movement_details_list
    }
    root_dir="root directory to save the dataframe"
    for df, data in data_dict.items():
            filename= df
            df=spark.createDataFrame(data)
            df.write.format('parquet').mode('overwrite').save(f"{root_dir}/{filename}/")
"""
    customer_df = spark.createDataFrame(customer_details_list) #schema=schema_for_customer_details)
    address_df = spark.createDataFrame(address_details_list) #schema=schema_for_address_details)
    membership_df = spark.createDataFrame(membership_details_list) #schema=schema_for_membership_details)
    product_df = spark.createDataFrame(product_details_list)
    productCostHis_df= s #schema=schema_for_product_details)
    # Create DataFrames for other entities similarly """



# Define schema for DataFrames if needed
# Replace `schema_for_customer_details`, `schema_for_address_details`, etc., with actual schemas
""" schema_for_customer_details = ...
schema_for_address_details = ...
schema_for_membership_details = ...
schema_for_product_details = ...

"""
# Define schemas for other DataFrames similarly

# Call the function to generate data for one hour
genData = generate_data_for_one_hour()

print("Data generation and writing to Lakehouse completed.")
