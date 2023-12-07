#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>



/////////////////////////////////////////////////////////////////


// Inculding the getline function to read a string of text 
int getline(char **lineptr, size_t *n, FILE *stream) {
	static char line[256];
	char *ptr;
	unsigned int len;


   if (lineptr == NULL || n == NULL) {
      errno = EINVAL;
      return -1;
   }

   if (ferror (stream))
      return -1;

   if (feof(stream))
      return -1;
     
   fgets(line,256,stream);

   ptr = strchr(line,'\n');   
   if (ptr)
      *ptr = '\0';

   len = strlen(line);
   
   if ((len+1) < 256) {
      ptr = realloc(*lineptr, 256);
      if (ptr == NULL)
         return(-1);
      *lineptr = ptr;
      *n = 256;
   }

   strcpy(*lineptr,line); 
   return(len);
}

struct Product  // Product Struct for product informations
{
	char* name; // name refers to a pointer, so when dereferenced, name is a char. In this case a pointer initialized to a string located in read-only memory.
	double price; //  Double = decimal number
};

struct ProductStock // ProductStock Struct for stock informations
{
	struct Product product;
	int quantity;
};

struct Shop // Shop Struct for shop infomations
{
	double cash;
	struct ProductStock stock[20];
	int index;
};

struct Customer // Customer Struct for customer informations
{
	char* name;
	double budget;
	struct ProductStock shoppingList[10]; // Nested struct - An Array of 10 elements.
	int index;
};


// ============================================================================================================================================================================

// printProduct() function will be used to print product informations
void printProduct(struct Product p)
{
	printf("Product: %s \nProduct: %.2f \n", p.name, p.price); // Print the product name and its price.
	printf("\n");
}


// Function to print main shop menu
void menuOptions() {
	
	printf("##########################################################\n");
	printf("\t\t\tGENERAL STORE\t\t\n");
	printf("##########################################################\n");
	
	printf("\n\nWelcome to the general store. How can we help you today?\n\n");
    printf("\t-[1] View shop\n");
    printf("\t-[2] Place an order\n");
    printf("\t-[3] Import Order from a file\n");
    printf("\t-[0] Exit\n");	
}

struct Shop createAndStockShop()
{
	FILE *fp;
	char *line = NULL;
	size_t len = 0;
	ssize_t read;
	char *filename = "C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/shop.csv"; 

	// Try to open and read the csv
	fp = fopen(filename, "r");
	if (fp == NULL) {
		fprintf(stderr, "cannot open %s: \n", filename);
		exit(EXIT_FAILURE);
	}
	
	getline(&line, &len, fp);
	// read cash in 
	double cashInshop = atof(line);
	struct Shop shop = { cashInshop };


	while ((read = getline(&line, &len, fp)) != -1)
	{
            char *n = strtok(line, ",");
            char *p = strtok(NULL, ",");
            char *q = strtok(NULL, ",");
            // convert to datatypes
            double price = atof(p);
            int quantity = atoi(q);
            char *name = malloc(sizeof(char)*50);
            strcpy(name, n);

			
            struct Product product = {name, price};
            struct ProductStock stockItem = {product, quantity};
            shop.stock[shop.index++]=stockItem;
    }

	return shop;
}

void printShop(struct Shop s) // This will print shop details
{
	printf("\n\n\n------------------------------------------------------------\n                  WELCOME TO THE 'C' SHOP \n------------------------------------------------------------\n ");
	printf("**********************************************************\n");

    printf("\n");
	printf("============================================================\n");
    printf("   Cash in the Shop: EUR %.2f \n", s.cash); // print how much cash Store has in cash. Taken from stock.csv file
    printf("============================================================\n");
	printf("   Credit/Debit card payments acceptable in this Shop\n"); // just to inform customers that card payments are avilable
	printf("============================================================\n");
	printf("\n");
	printf("\n");
    printf("\n*** STOCK AVAILABLE IN 'C' SHOP ***\n");
    printf("\n");

	for (int i = 0; i < s.index; i++) // 'for' loop displays the stock details to the output
	{
		
		printProduct(s.stock[i].product);
		printf("Quantity: %d\n", s.stock[i].quantity); // When you press 1st option in Menu selection, this quantity will be given as output.

		printf("-------------------------------------------------------\n");
	}
};

struct Customer customerOrder() // this struct will read order.csv file  
{
	FILE * fp;
    char filepath[250];
	char * line = NULL;
	size_t len = 0;
	size_t read;


	// Try to open and read csv file
	fp = fopen("C:/Users/odonovanm/Desktop/programming/Multi Paradigm Programming/customer1.csv","r");
    if (fp == NULL) {
        printf("Error %s\n", strerror(errno));
        exit(100);
    }

	getline(&line, &len, fp); // read customer name and budget, so csv file
	
	char *n = strtok(line, ",");
    char *b = strtok(NULL, ",");
	
	char *name = malloc(sizeof(char)*50); //create a local token string variable
    strcpy(name, n);
	double budget = atoi(b);
	struct Customer c ={ name, budget };
	
	
    while ((read = getline(&line, &len, fp)) != -1)
    {
            char *r = strtok(line, ",");
			char *q = strtok(NULL, ",");
			int quantity = atoi(q);
			char *productname = malloc(sizeof(char)*50);
			strcpy(productname, r);
			struct Product product = {productname};
			struct ProductStock orderItem = {product, quantity};
			c.shoppingList[c.index++]=orderItem;
        }

    return c;
}

//================================================================================================================================

// printCustomer() will be used to print customer's details and order
void printCustomer(struct Customer c) 
{
	printf("\n=======================================================");
	printf("\nCustomer: %s \nCustomer: EUR %.2f\n", c.name, c.budget); // Prints customer's name and budget
    printf("=======================================================\n");
	printf("\n");

	for (int i = 0; i < c.index; i++) // Start loop through each of the items in the shopping list 
	{
		printProduct(c.shoppingList[i].product); // Print the product informations
		printf("The customer wants %d of the above\n", c.shoppingList[i].quantity);
		printf("\n-------------------------------------------------------\n");
	}
}

// =====================================================================================================================================

// searching both and comparing and returning price
double findPrice(struct Shop s, struct Customer c)
{
       
	struct Product productcustomer;
	double sum =0;
	double shortamount;
	
    printf("\n");
    printf("\n=======================================================\n");
	printf("\n      ***  Total to pay by customer  ***  \n");
    printf("=======================================================\n");
    printf("\n");

	for (int i = 0; i < s.index; i++)
	{
		for (int j = 0; j < c.index; j++) // loop through customer order
		{
			struct Product product = s.stock[i].product;
			struct Product productcustomer = c.shoppingList[j].product;

			if (strcmp(product.name, productcustomer.name) == 0)
			{ 
					
                   printf("Product: %s\nPrice: EUR %.2f * Quantity %d\n", c.shoppingList[j].product.name, product.price, c.shoppingList[j].quantity);
				    // check if in stock in store
					printf("In stock: %s, availability: %d\n", c.shoppingList[j].product.name, s.stock[i].quantity);
					printf("-------------------------------------------------------\n");
                    printf("\n");


					if(s.stock[i].quantity < c.shoppingList[j].quantity) // check if Shop has the item quantity
					{
                        printf("Sorry, the Shop has only %d\n \n", s.stock[i].quantity); // if not in stock
                        printf("-----------------------------------------------------\n");
                    }
                    else{
					sum = product.price * c.shoppingList[j].quantity + sum; // adding up the bill
					s.stock[i].quantity = s.stock[i].quantity - c.shoppingList[j].quantity;
					
					//i++;		
					}
 
            }	
		}
	}

        if(c.budget< sum)
		{
			shortamount = (sum - c.budget);
			printf("-----------------------------------------------------------------------------------------\n");
			printf("We are sorry, but you do not have enough money - you will need: EUR %.2f more\n", shortamount);
			printf("-----------------------------------------------------------------------------------------\n");
			printf("=========================================================================================\n");
							
		}
		else if(shortamount==0){
            printf("-----------------------------------------------------------------------------------------\n");
			printf("We are sorry, but we do not have this product\n");
			printf("-----------------------------------------------------------------------------------------\n");
			printf("=========================================================================================\n");
        } 
        
        else {
			printf("\n");
			printf("Total to pay by customer: EUR %.2f\n", sum);
            printf("===================================\n");
            printf("\n\n");
            printf("=======================================================\n");
			
            printf("\n*** Cash and availability of products in the Shop ***  \n");
            printf("=======================================================\n");
            printf("\n");
			
			
			s.cash = s.cash + sum; // add customer's bill to the shop's float
			printf("Cash has been updated and now is: EUR %.2f\n", s.cash);
			printf("\n-------------------------------------------------------\n");
			// for (int i = 0; i < s.index; i++)
			// {
			// 	printf("Product's name: %s\nProduct's quantity after shopping: %d \n",s.stock[i].product.name, s.stock[i].quantity );
            //     printf("\n");
            // }

		}

	return -1; 
}


// ========================================================================================================================================
struct Customer orderlive(struct Shop s)
{
	printf("\n");
	printf("Welcome to the general store. What's your name? "); // live Shop will ask for your name
	char *name = malloc(sizeof(char)*50);
    scanf(" %s", name);

	printf("\n");
	printf("Hi %s, what's your budget? ", name); // live Shop will ask for budget
	double budget;
	scanf("%lf", &budget);
	

    printf("\nPerfect. Please choose from our product list:\n");
    printf("*********************************************\n");
    printf("\t\tCatalogue");
	printf("\n_____________________________________________\n");
    printf("\n Product\t\tPrice\n");
    printf("*********************************************\n");
	
	// Loop through shop stock and print product name and price
	for (int i = 0; i < s.index; i++) {    
        printf("%s\t\t%.2f\n---------------------------------------------\n", s.stock[i].product.name, s.stock[i].product.price);	
    }
    
    printf("\n");
	printf("What would you like to buy? "); // live Shop will ask for product you would like to buy
	char *p = malloc(sizeof(char)*50);
	char temp;
	scanf("%c", &temp); 
	scanf("%[^\n]s", p); 
	  
	printf("\n");
	printf("How many would you like to buy? "); // live Shop will ask how many products ypu would like to buy
	int q;
	scanf(" %d", &q);
	
    struct Customer nc ={name, budget};
	struct Product product = {p};
	struct ProductStock orderItem = {product, q};
	nc.shoppingList[nc.index++]=orderItem;
	printf("\nThe balance on %s's account is € %.2f\n", nc.name, nc.budget);
	printf("------------------------------------------------------");
    printf("------------------------------------------------------");
	
   return nc;
}
	

// Function for the main menu
void displayMenu(struct Shop shop) {
	
    menuOptions(); // Show main shop menu


    printf("\nPlease select an option: ");
    char choice; // Variable to store users choice from menu
    scanf("%s", &choice);
	
    
    if (choice == '1') { // Display shop // 
			
		printShop(shop); // Print shop
        displayMenu(shop); // Return to main menu
	}
        
    else if (choice == '2') { // Place a live order //

        struct Customer nc = orderlive(shop); //Create a customer from live input
        printCustomer(nc); //Print the customer
        findPrice(shop, nc );// Process the order by calling processOrder 
        displayMenu(shop) ;

	} 
		
	else if (choice == '3') { // Read order from a csv file //
		
        struct Customer c = customerOrder();
        printCustomer(c);
        
        findPrice(shop, c);
        displayMenu(shop) ;
	} 

	else if (choice == '0') { // Exit programme //
			
		printf("Thanks for shopping at the general store, goodbye!"); 
		exit(0);
	} 
        
    else {
          
        displayMenu(shop); // Any other key is pressed show main menu
	}
}



int main(void) {

	struct Shop shop = createAndStockShop(); // Stock the shop
	displayMenu(shop); // Show the display menu
    return 0;
}