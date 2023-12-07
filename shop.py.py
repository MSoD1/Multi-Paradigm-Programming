# Import libaries
from dataclasses import dataclass, field   
from typing import List                    
import csv                                


#/////////////////////////////////////////////////////////////////#


# Equivalent to c structs or OOP classes
@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shoppingList: List[ProductStock] = field(default_factory=list)



#/////////////////////////////////////////////////////////////////#


# Function to stock the shop by reading in the stock.csv file
def createAndStockShop():
    s = Shop()
    
    # Try to open and read the csv file
    try:
        with open("C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/shop.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            s.cash = float(first_row[0]) # First row = shop cash   
            # Iterate through rows and create Product, ProductStock and stock instances 
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, int(row[2]))
                s.stock.append(ps)
        return s # Return shop datacase
    
    except FileNotFoundError:
        print(f"Cannot open {csv_file}")
       

# Function to print product name and price
def printProduct(p):
    print(f'{p.name}\t\t{p.price:,.2f}')



# Function to display the shop
def printShop(s):
    print('##########################################################\n')
    print('\t\tGENERAL STORE OVERVIEW\t\t\n')
    print('##########################################################\n')
    print(f"Shop Cash: {s.cash:.2f}")
    print("*********************************************\n")
    print("\t\tCatalogue")
    print("*********************************************")
    print("\n Product\t\tPrice\t\tQty")
    print("_____________________________________________\n")
    
    #  Loop through each stock item and print name, price and qty
    for item in s.stock:
        print(f"{item.product.name} \t\t{item.product.price:.2f}\t\t{item.quantity}\n")
        print("----------------------------------------------\n")




# Function to read a customer's order from a csv file
def customerOrder():

    # Try to open and read csv file
    try:
        with open("C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/customer1.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            c = Customer(first_row[0], float(first_row[1])) # Create customer class
            # Create customer shoppingList by iterating through the rest of the csv
            for row in csv_reader: 
                name = row[0]
                quantity = int(row[1]) 
                p = Product(name) 
                ps = ProductStock(p, quantity) 
                c.shoppingList.append(ps) # Add to shoppingList      
              
            return c # Return customer

    except FileNotFoundError:
        print(f"Cannot open {csv_file}")




# Function to print customer 
def printCustomer(c,s):
    
    total = 0 # Variable to track customer order total
    
    print("##########################################################\n")
    print(f" Customer: {c.name}\n Budget:   {c.budget:.2f}\n")
    print("***************************************************\n")
    print("\n Product\t\tPrice\tQty\tUnit Total")
    print("___________________________________________________\n")
    

    # Loop through shoppingList
    for item in c.shoppingList:

        getPrice(c, s) # Calling the getPrice function
        cost = 0 # Variable to track unit cost of a product
        
        # Comparing customer items to see if it exists in the shop stock
        for customerItem in s.stock:   
            if item.product.name.lower() == customerItem.product.name.lower():
                # Get the unit cost of the product (quantity x price) if it's in stock. Cost is 0 if item is not in stock
                cost =+ item.quantity * customerItem.product.price 

            
        print(f"{item.product.name}\t\t{item.product.price:.2f}\t{item.quantity}\t{cost:.2f}")
        print("---------------------------------------------------\n")
                
        total += cost # Update total cost		

    print(f"Total\t\t\t\t\t{total:.2f}")
    print("---------------------------------------------------\n")



# Function to get a product price
def getPrice(c, s):
    # Loops through the shop stock to find a match and retrieves the product price 
    for shopProduct in s.stock:
        for item in c.shoppingList:
            if (item.product.name.lower() == shopProduct.product.name.lower()):
                item.product.price = shopProduct.product.price
        


# Function to process customer order
def processOrder(shop, customer):
 
    # Variable to track whether to checkout a customers order
    #checkout = input(f"\nCheckout {customer.name}'s order? (y/n): ").lower()
    
    #if checkout == 'y':
        
    print("\n -------------------------------------------------\n")
    print("\n Checkout complete!\n")

        # Iterate over the customer shoppingList 
    for item in customer.shoppingList:
            
            # Process order
        for customerItem in s.stock:
                # if the item is a shop stock item calculate order total
            if item.product.name.lower() == customerItem.product.name.lower():

                orderTotal = item.quantity * customerItem.product.price

                    # If customer orders less than or equal to the the shop has in stock  
                if item.quantity <= customerItem.quantity:       
                        # and the order total is less than or equal the customers budget 
                    if customer.budget > orderTotal:
                            # Update the shop stock  
                        customerItem.quantity -= item.quantity
                            # Update the shop and customers cash
                        shop.cash += orderTotal
                        customer.budget -= orderTotal

                    else: # If the order total is more than the customers budget
                        print("\n***************************************************************\n")
                        print(f"\nWe are sorry, but you do not have enough money - you will need: EUR{(orderTotal):.2f}\n")
                        print("\n***************************************************************\n")
                                
                else: # If customer orders more than is stocked in the shop
                    print("\n***************************************************************\n");
                    print("\n Sorry, the Shop has only {} {}'s in stock\n".format(customerItem.quantity, customerItem.product.name));	
                    print("\n***************************************************************\n");  
            


#  Function to get customer name, budget and shopping list (live order)
def liveCustomer(shop):

    # Get customer name ad budget from input
    customerName = input("Welcome to the general store. What's your name? ") 
    customerBudget = float(input(f"Hi {customerName}, what's your budget? ")) 

    print("\nPerfect. Please choose from our product list:\n")
    print("*********************************************\n")
    print("\t\tCatalogue")
    print("_____________________________________________")
    print("\n Product\t\tPrice\n")
    print("*********************************************\n")

    # Loop through shop stock and print product name and price
    for i in shop.stock:
        printProduct(i.product)
        print("---------------------------------------------\n")


    live_customer = Customer(customerName, customerBudget) # Create Customer class instance


    #addItem = 'y' # Varaible to track if customer wishes to add additional products
    
    # Continue the while loop until the customer is finished adding items by pressing 'n' to adding additional items
    #while addItem != "n":

    # Create customer shoppingList #

        # Get product name and order quantity from input
    customerItem = input("\nWhat product would you like? ").lower()
        
    while True:
        try:
            customerQuantity = int(input("How many would you like to buy? "))
            break
        except ValueError:
            print("Please enter your budget as an number\t")
        

    p = Product(customerItem) # Check product name
    ps = ProductStock(p, customerQuantity) # Check order quantity
    live_customer.shoppingList.append(ps) # Add to shoppingList
  
        # Continue the while loop until the customer is finished adding items
        #addItem = input("Do you need anything else? (y/n): ").lower()
    
    return live_customer # Return customer



# Function to show main shop menu options
def menuOptions():

    print('##########################################################\n')
    print('GENERAL STORE\n')
    print('##########################################################\n')
    print("\nWelcome to the general store. How can we help you today?\n")
    print("\t[1] View shop")
    print("\t[2] Place an order")
    print("\t[3] Import Order from a file")
    print("\t[0] Exit")
    



# Function for main shop menu
def displayMenu(shop):
    
    menuOptions() # Show main menu
    
    while True:

        choice = input("\nPlease select an option: ") # Variable to track customer choice
        
        
        if choice == '1': # Display shop #

            printShop(shop) # Print the shop
            displayMenu(shop) # Return to main menu
            

        elif choice == '2': # Place a live order #

            live_customer = liveCustomer(shop) # Create a customer from live input
            printCustomer(live_customer, shop) # Print the customer
            processOrder(shop, live_customer ) # Process the order by calling processOrder 
            print("\nThe balance on {}'s account: EUR {:.2f}\n".format(live_customer.name, live_customer.budget)) # Print customers new balance
    
            displayMenu(shop) # Return to main menu


        elif choice == '3': # Read order from a csv file #

            customer = customerOrder() # Create a customer from csv file
            printCustomer(customer, shop) # Print the customer
            processOrder(shop, customer) # Process the order by calling processOrder 
            print("\nThe balance on {}'s account: EUR {:.2f}\n".format(customer.name, customer.budget)) # Print customers new balance
            displayMenu(shop) # Return to main menu
            

        elif choice == '0': # Exit programme #
            print("Thanks for shopping at the general store, goodbye!")
            exit()  # Break out of display menu loop         


        else:
            displayMenu(shop) # Any other key is pressed show main menu




s = createAndStockShop() # Stock the shop
displayMenu(s) # Show the display menu