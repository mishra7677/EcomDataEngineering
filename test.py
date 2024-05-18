from datetime import date, datetime, timedelta
import pandas as pd
from faker import Faker
import os 
from dotenv import load_dotenv

load_dotenv()

f=Faker()
BASE_DIR= os.getenv('BASE_DIR')


class customer:
    
    def __init__(self):
        self.custID=f.random_int(min=1, max=999999999999)
    
    def customerDetails(self):
        customerData={
            'custID':self.custID,
            'value': {
                'Name': f.name(),
                'age': f.random_int(min =16, max= 80),
                'gender': f.passport_gender(),
                'email': f.email(),
                'phoneNumber': f.basic_phone_number()
            }
        }
        return customerData
    
    def AddressDetails(self):

        addressData = {
            'custID': self.custID,
            'StreetAddress': f.street_address(),
            'City': f.city(),
            'State': f.state(),
            'ZipCode': f.zipcode(),
            'Country': f.country()
        }
        return addressData

    def membershipDetails(self):
        current_date = datetime.today()
        min_start_date= current_date - timedelta(days= 3650)
        max_end_date = current_date + timedelta(days=365)  # Maximum 12 months from today

        membershipData = {
            'custID': self.custID,
            'MembershipID': f.random_int(min=1, max=999999999),
            'Level': f.random_element(elements=('Silver', 'Gold', 'Platinum')),
            'Start_date': f.date_between(start_date=min_start_date, end_date=current_date),
            'End_date': f.date_between(start_date=current_date, end_date=max_end_date)
        }
        return membershipData



class Product:
    
    def productDetails(self):
        productData = {
            'ProductID': f.random_int(min=1000, max=9999),
            'ProductName': f.company(),
            'Category': f.random_element(elements=('Electronics', 'Clothing', 'Books', 'Furniture')),
            'Description': f.text()
        }
        return productData

    def productCostHistory(self):
        costHistory = []
        for _ in range(5):  # Generate cost history for 5 periods
            costData = {
                'Date': f.date_this_decade(),
                'Cost': f.random_int(min=10, max=1000)  # Random cost range
            }
            costHistory.append(costData)
        return costHistory

    def productLocation(self):
        locationData = {
            'LocationID': f.random_int(min=100, max=999),
            'LocationName': f.street_name(),
            'City': f.city(),
            'State': f.state(),
            'Country': f.country()
        }
        return locationData

class cart:

    def cartDetails(self):
        pass

    def cartDiscount(self):
        pass

class shipping:

    def shippingDetails(self):
        pass

class order:

    def orderDetails(self):
        pass

    def returnOrderDetails(self):
        pass

    def exchangeOrderDetails(self):
        pass


class inventory:
    
    def inventoryDetails(self):
        pass

    def supplierDetails(self):
        pass

    def stockMovementDetails(self):
        pass 
    

