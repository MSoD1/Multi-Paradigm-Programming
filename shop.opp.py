# Import libaries
import csv


#/////////////////////////////////////////////////////////////////#

# Equivalent to c structs or python dataclasses

# Product class
class Product:
    def __init__(self, name, price=0):
        self.name = name.lower()
        self.price = price
    
    # Returns name and price
    def __repr__(self): 
        return f'{self.name}\t\t{self.price:.2f}'


#/////////////////////////////////////////////////////////////////#

# ProductStock class
class ProductStock:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    # Method to get product name
    def productName(self):
        return self.product.name

     # Method to get product price
    def productPrice(self):
        return self.product.price

    # Method to get cost (price x quantity)
    def cost(self):
        return self.productPrice() * self.quantity

    # Method to get product quantity
    def productQuantity(self):
        return self.quantity

    # Method to update shop quantity when an item is sold
    def updateQuantity(self, customerQuantity):
        self.quantity -= customerQuantity

    # Method to get the product
    def getProduct(self):
        return self

   # Returns the product and its quantity
    def __repr__(self):
        return f"{self.product}\t{self.quantity:.0f}"
 

#/////////////////////////////////////////////////////////////////#


# Customer class
class Customer:
    def __init__(self):

        # Empty list to hold customer's order
        self.shoppingList = []
 
        # Try to open and read csv
        try:
            with open("C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/customer1.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                first_row = next(csv_reader)
                self.name = first_row[0]
                self.budget = float(first_row[1])
                for row in csv_reader:
                    name = row[0]
                    quantity = float(row[1])
                    p = Product(name)
                    ps = ProductStock(p, quantity)
                    self.shoppingList.append(ps)
                return

        except FileNotFoundError:
                print(f"Cannot open {csv_file}") 
                return
                    
            


    # Method to calculate cost of customers shopping list
    def getPrice(self, priceList):
         # Iterate through the customer shopping list and shop stock, if there's a match get the name and price
        for shopProduct in priceList:
            for customerItem in self.shoppingList:
                if (customerItem.productName() == shopProduct.productName()):
                    customerItem.product.price = shopProduct.productPrice()
    
    
    # Method to get the cost
    def total(self):
        cost = 0 # Variable to track the cost
        # Get the total cost of the order using the cost method from the productStock class
        for customerItem in self.shoppingList:
            cost += customerItem.cost()
        return cost



# Returns customers shopping list with unit and total cost
    def __repr__(self):
        print("##########################################################\n")
        print(f'Customer: {self.name} \nBudget: {self.budget:.2f}')
        print("***************************************************")
        print("\n Product\t\tPrice\tQty\tUnit Total")
        print(f"___________________________________________________\n")

        str = f""

        for item in self.shoppingList:
            
            cost = item.cost()
            str += f"{item}\t"
            
            str += f"{cost:.2f}\n"
            str += "---------------------------------------------------\n\n"

        str += f"Total\t\t\t\t\t {self.total():.2f}\n"       
        str += "---------------------------------------------------\n"     
            
        return str 


#/////////////////////////////////////////////////////////////////#       


# Live class (subclass of Customer)
class Live(Customer):
    def __init__(self):

        print('##########################################################\n')
        print('\t\t\tGENERAL STORE\t\t\n')
        print('##########################################################\n')

        self.shoppingList = [] # Empty list to hold customer order

        # Get customers name and budget for a live order
        self.name = input("Welcome to the general store. What's your name? ") 

        while True:
            try:
                self.budget = float(input(f"Hi {self.name}, what's your budget? ")) 
                break
            except ValueError:
                print("Please enter your budget as an number\t")
        
       

        print("\nPerfect. Please choose from our product list:\n")
        # Print out shop product list for customer
        print("*********************************************\n")
        print("\t\tCatalogue")
        print("_____________________________________________")
        print("\nProduct\t\t\tPrice")
        print("*********************************************\n")
        print("Coke\t\t0.55\n---------------------------------------------\n")
        print("Bread\t\t0.70\n---------------------------------------------\n")
        print("Coffee\t\t1.20\n---------------------------------------------\n")
        print("Sauce\t\t0.80\n---------------------------------------------\n")

        

            
        # Get the customers product order and quantity
        product = input("\nWhat would you like to buy?  ").lower()


        while True:
            try:
                quantity = int(input("How many would you like to buy? "))
                break

            except ValueError:
                print("Please enter the quantity as an integer")
            

        p = Product(product)
        ps = ProductStock(p, quantity)
        self.shoppingList.append(ps)



#/////////////////////////////////////////////////////////////////#

# Shop class 
class Shop:
    def __init__(self, path):
        
        self.stock = [] # Empty list to hold the shop stock

        # Open and read csv
        with open("C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/shop.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)


    # Returns the shop
    def __repr__(self):
        str = ""
        print('##########################################################\n')
        print('\t\tGENERAL STORE OVERVIEW\t\t\n')
        print('##########################################################\n')

        str += (f"Shop Cash: {self.cash:.2f}\n*********************************************\n\t\tCatalogue\n*********************************************\n\n Product\t\tPrice\tQty\n_____________________________________________\n")
        
        for item in self.stock:
            str += f"{item}\n\n----------------------------------------------\n"
        
        return str       



    # Method to process a customers order
    def processOrder(self,c):
        
 
        print("\n -------------------------------------------------\n")
        print("\n Checkout complete!\n")
       
        self.totalProductCost = 0 # Variable to track customers total

            # Loop through customers order; check items are in stock, update shop cash and stock if order successful
        for customerItem in c.shoppingList:
            self.checkStock(customerItem)
            self.updateCash(c)
            self.updateStock(self.product)
           
        print(f"\nThe balance on {c.name}'s account: EUR {c.budget:.2f}\n")
           


    # Method to update customer cash      
    def updateCash(self,c):
        # If customer budget is less than the order total 
        if c.budget < self.totalProductCost: 
            print("\n***************************************************************\n")
            print(f"\nWe are sorry, but you do not have enough money - you will need: EUR {(self.totalProductCost):.2f}\n")
            print("\n***************************************************************\n")

        else: # Otherwise update customers cash
            self.cash += self.totalProductCost
            c.budget -= self.totalProductCost
 
           
    # Method to check customers order vs stock in shop
    def checkStock(self,customerItem):
        for shopProduct in self.stock:
            # If customer item is in the shop stock get the product details so the stock quantity can be checked
            if (customerItem.productName() == shopProduct.productName()): 
                self.product_name = shopProduct.productName()
                self.product = shopProduct.getProduct()
               
                # If customer orders less than or equal to the the shop has in stock, get the product unit cost and qty order (reduce shop stock later)
                if customerItem.quantity <= shopProduct.quantity:
                    self.totalProductCost = customerItem.quantity * shopProduct.product.price
                    self.customerQuantity = customerItem.quantity
                    return self.totalProductCost, self.product, self.customerQuantity, self.product_name
   
                # If the customer orders more than is in stock
                elif (customerItem.quantity > shopProduct.quantity):
                    print("\n***************************************************************\n")
                    print(f"\n Sorry, the Shop has only {shopProduct.quantity} {self.product.productName()}'s in stock\n");	
                    print("\n***************************************************************\n")
                    
                else:
                    print("\n***************************************************************\n")
                    print(f"\n We are sorry, but we do not have this product\n");	
                    print("\n***************************************************************\n")


    # Method to update shop stock after customer order
    def updateStock(self, product):
        product.updateQuantity(self.customerQuantity)



    #/////////////////////////////////////////////////////////////////#     

    # Method for main shop menu
    def displayMenu(self):

        while True:
            
            print('##########################################################\n')
            print('\t\t\tGENERAL STORE\t\t\n')
            print('##########################################################\n')
            print("Welcome to the general store. How can we help you today?\n")
            print("\t-[1] View shop")
            print("\t-[2] Place an order")
            print("\t-[3] Import Order from a file")
            print("\t-[0] Exit")


            self.choice = input("\nPlease select an option: ") # Variable to track customer choice


            if (self.choice == "1"): # Display shop #

                print(self) # Print the shop
                self.displayMenu() # Return to main menu


            elif (self.choice == "2"):  # Place a live order #
               
                c = Live() # Call Live class to create a customer object
                c.getPrice(self.stock) # Calculate total cost of customer's order, passing shop stock to the getPrice method
                print(c) # Print the customer
                self.processOrder(c) # Process the order by calling processOrder method on the customer object
                self.displayMenu() # Return to main menu


            elif (self.choice == "3"):  # Read order from a csv file #
                
                c = Customer() # Call Customer class, creates a customer object
                c.getPrice(self.stock) # Calculate total cost of customer's order, passing shop stock to the getPrice method
                print(c)   # Print the customer
                self.processOrder(c) # Process the order by calling processOrder method on the customer object
                self.displayMenu() # Return to main menu


            elif(self.choice == "0"): # Exit programme #

                print("Thanks for shopping at the general store, goodbye!")
                exit() # Break out of display menu loop
            

            else:
                self.displayMenu() # Any other key is pressed show main menu
                



#/////////////////////////////////////////////////////////////////#


# Main function for when the programme executes 
def main():
   
    s = Shop("C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/shop.csv") # Stock the shop
    s.displayMenu() # Show the display menu


if __name__ == "__main__":

    main()