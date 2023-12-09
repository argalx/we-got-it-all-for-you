import sqlite3

# Database connection
conn = sqlite3.connect('we-got-it-all-for-you/sm.db')

# Create cursor object
cursor = conn.cursor()

# SM Table Creation

# invoices
cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
               id INTEGER PRIMARY KEY,
               invoice TEXT NOT NULL,
               sales_rep_id INTEGER NOT NULL,
               customer_id INTEGER NOT NULL
    )
''')

# sales_reps
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales_reps (
               id INTEGER PRIMARY KEY,
               full_name TEXT NOT NULL
    )
''')

# customers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
               id INTEGER PRIMARY KEY,
               full_name TEXT NOT NULL
    )
''')

# invoice_details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoice_details (
               id INTEGER PRIMARY KEY,
               invoice_id INTEGER NOT NULL,
               product_id INTEGER NOT NULL
    )
''')

# products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
               id INTEGER PRIMARY KEY,
               product TEXT NOT NULL,
               vendor_id INTEGER NOT NULL
    )
''')

# vendors
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendors (
               id INTEGER PRIMARY KEY,
               vendor TEXT NOT NULL
    )
''')

# Insert Function
def inserData():
    salesReps = ['Im Na-yeon', 'Park Ji-hyo', 'Mina Myoi', 'Kim Da-hyun', 'Son Chae-young']
    customers = ['Taichi Nishimura', 'Setsu Suzaki', 'Arnos Voldigoad', 'Rimuru Tempest']
    vendors = ['Shellsoft Technology Corporation', 'Krayon', 'iAlchemy', 'Fujitsu']
    vendorProducts = {'Shellsoft Technology Corporation': ['Power Apps', 'Power Automate', 'Power BI'], 'Krayon':['Power Virtual Agent', 'Power Pages'], 'iAlchemy':['Azure Synapse', 'Azure Data Factory'], 'Fujitsu':['SharePoint Online', 'OneDrive']}
    invoices = {'Invoice 1':{'customer': 'Taichi Nishimura', 'sales': 'Park Ji-hyo', 'products':['Power Apps','Power BI','SharePoint Online']},'Invoice 2':{'customer': 'Setsu Suzaki', 'sales': 'Mina Myoi', 'products': ['Power Apps', 'SharePoint Online', 'Azure Synapse']}, 'Invoice 3':{'customer': 'Arnos Voldigoad', 'sales': 'Im Na-yeon', 'products':['Power Virtual Agent', 'Power Automate']}}


    # Insert Sales Reps
    for sales in salesReps:
        cursor.execute('INSERT INTO sales_reps (full_name) VALUES (?)',(sales,))

    # Insert Customers
    for customer in customers:
        cursor.execute('INSERT INTO customers (full_name) VALUES (?)',(customer,))
    
    # Insert Vendors
    for vendor in vendors:
        cursor.execute('INSERT INTO vendors (vendor) VALUES (?)',(vendor,))

    # Insert Products
    for vendor, products in vendorProducts.items():
        # Get Vendor ID
        cursor.execute('SELECT id FROM vendors WHERE vendor=?',(vendor,))
        vendorDetail = cursor.fetchall()
        vendorId = list(vendorDetail[0])[0]

        for product in products:
            cursor.execute('INSERT INTO products (product, vendor_id) VALUES (?, ?)',(product, vendorId,))

    # Invoice and Invoice Details
    for invoice, invoiceDetails in invoices.items():
        # Get Sales Rep ID
        cursor.execute('SELECT id FROM sales_reps WHERE full_name=?',(invoiceDetails.get('sales'),))
        salesDetail = cursor.fetchall()
        salesId = list(salesDetail[0])[0]
        
        # Get Customer ID
        cursor.execute('SELECT id FROM customers WHERE full_name=?',(invoiceDetails.get('customer'),))
        customerDetail = cursor.fetchall()
        customerId = list(customerDetail[0])[0]

        # Insert Invoice
        cursor.execute('INSERT INTO invoices (invoice, sales_rep_id, customer_id) VALUES (?, ?, ?)',(invoice, salesId, customerId,))

        # Invoice Details
        for product in invoiceDetails.get('products'):
            # Get Invoice ID
            cursor.execute('SELECT id FROM invoices WHERE invoice=?',(invoice,))
            invoiceDetail = cursor.fetchall()
            invoiceId = list(invoiceDetail[0])[0]
            
            # Get Product ID
            cursor.execute('SELECT id FROM products WHERE product=?',(product,))
            productDetail = cursor.fetchall()
            productId = list(productDetail[0])[0]

            # Insert Invoice Details
            cursor.execute('INSERT INTO invoice_details (invoice_id, product_id) VALUES (?, ?)',(invoiceId, productId,))

    # Commit Changes
    conn.commit()

# Display Function
def displayData():
    # Get Invoices
    cursor.execute('SELECT * FROM invoices')
    invoices = cursor.fetchall()

    for invoice in invoices:
        # Invoice
        invoiceTitle = list(invoice)[1]
        
        # Sales Rep
        cursor.execute('SELECT full_name FROM sales_reps WHERE id=?',(list(invoice)[2],))
        salesDetail = cursor.fetchall()
        sales = list(salesDetail[0])[0]

        # Customer
        cursor.execute('SELECT full_name FROM customers WHERE id=?',(list(invoice)[3],))
        customerDetail = cursor.fetchall()
        customer = list(customerDetail[0])[0]

        # Invoice Details

        # Invoice Details Header
        print(f"{'x'*100}\nINVOICE DETAILS\n{'-'*100}\nInvoice: {invoiceTitle}\nSales: {sales}\nCustomer: {customer}\n{'-'*100}\nORDERS\n{'-'*100}\n{'Product':<30}{'Vendor':>20}")

        # Get Invoice Details
        cursor.execute('SELECT product_id FROM invoice_details WHERE invoice_id=?',(list(invoice)[0],))
        invoiceDetails = cursor.fetchall()

        # Get Products and Vendors
        for products in invoiceDetails:
            # Product
            cursor.execute('SELECT product, vendor_id FROM products WHERE id=?',(list(products)[0],))
            productDetails = cursor.fetchall()
            product = list(productDetails[0])[0]
            
            # Vendor
            cursor.execute('SELECT vendor FROM vendors WHERE id=?',(list(productDetails[0])[1],))
            vendorDetails = cursor.fetchall()
            vendor = list(vendorDetails[0])[0]
            
            # Invoice Details Content
            print(f"{product:<30}{vendor:>20}")

# Insert Data Function
# inserData()

# Display Data Function
displayData()

# Close Connection
conn.close()