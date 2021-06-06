# Best Buy Bot
## Faris L Kapes 
### Installation

* Install Firefox from the following link:
  
        https://www.mozilla.org/en-US/firefox/download/

* Download Geckodriver from the following link and extract the downloaded archive into a known directory, such as your downloads folder.

    * On Mac OSX:
            
        * Add Geckodriver to your path directory:
            
                export PATH=$PATH:/path/to/downloaded/geckodriver
        
        * This may not solve the issue, so I have added the ability to change the path of the Geckodriver executable to the first line of the config.json file. It should follow this format:
        
                /path/to/your/geckodriver
    
        * Finally, you may find that you need to make the geckodriver file executable. So cd into the directory it is in and run the following command:
    
                chmod +x geckodriver
    
    * On Windows:
    
        * Simply fill in the field in config.json named executable_path with the path to the extracted Geckodriver.exe, following this format:
    
                C:/Users/path/to/geckodriver.exe
    
### Configuration For Signed In Use:
    
* All the following fields are mandatory for signed in purchasing and must follow the given example formatting.
    
    1. ####"bot_usage_case": Set this to:
            sign-in
       
    2. ####"url": Navigate to the product page on bestbuy.com and copy everything after the bestbuy.com
            "/site/evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6439299.p?skuId=6439299"
    
    3. ####"title": Copy the title of the item in full from the product page
            "EVGA - GeForce RTX 3070 XC3 ULTRA GAMING 8GB GDDR6 PCI Express 4.0 Graphics Card"
    
    4. ####"email": Use your BestBuy account email
            "abcd@gmail.com"
       
    5. ####"password: Use your BestBuy account password
            "password"
       
    6. ####"first_name": Use your first name for billing and shipping addresses
            "John"
       
    7. ####"last_name": Use your last name for billing and shipping addresses
            "Doe"
       
    8. ####"address": Use your street address, include number and street name for both billing and shipping addressees
            "223 Colombiana Road"
       
    9. ####"city": Use your city for both billing and shipping addressees
            "Birmingham"
       
    10. ####"state": Use your two letter state abbreviation for both billing and shipping addresses
            "AL"
    
    11. ####"zip_code": Use your five-digit zip code for both billing and shipping addresses
            "12345"
       
    12. ####"cvv": Use the security code on the back of your card
            "280"
    
    13. ####"cc_number": Use the 16 digit number on the front of your credit or debit card
            "1234456789012345"
    
    14. ####"month": Use the two digit month of your cards' expiry date
            "02"
    
    15. ####"year": Use the four digit year of your cards' expiry date
            "2022"
    
    16. ####"phone": Use your phone number for any updates that BestBuy may send.
            "8880912122"

### Configuration for Guest use:

* All the following fields are mandatory for Guest use:

    1. ####"bot_usage_case": Set this to:
            "guest"
       
    2. ####"url": Navigate to the product page on bestbuy.com and copy everything after the bestbuy.com
            "/site/evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6439299.p?skuId=6439299"
    
    3. ####"title": Copy the title of the item in full from the product page
            "EVGA - GeForce RTX 3070 XC3 ULTRA GAMING 8GB GDDR6 PCI Express 4.0 Graphics Card"
    
    4. ####"email": Use your BestBuy account email
            "abcd@gmail.com"
       
    5. ####"first_name": Use your first name for billing and shipping addresses
            "John"
       
    6. ####"last_name": Use your last name for billing and shipping addresses
            "Doe"
       
    7. ####"address": Use your street address, include number and street name for both billing and shipping addressees
            "223 Colombiana Road"
       
    8. ####"city": Use your city for both billing and shipping addressees
            "Birmingham"
       
    9. ####"state": Use your two letter state abbreviation for both billing and shipping addresses
            "AL"
    
    10. ####"zip_code": Use your five-digit zip code for both billing and shipping addresses
            "12345"
       
    11. ####"cvv": Use the security code on the back of your card
            "280"
    
    12. ####"cc_number": Use the 16 digit number on the front of your credit or debit card
            "1234456789012345"
    
    13. ####"month": Use the two digit month of your cards' expiry date
            "02"
    
    14. ####"year": Use the four digit year of your cards' expiry date
            "2022"
    
    15. ####"phone": Use your phone number for any updates that BestBuy may send.
            "8880912122"

### To Do List:
    
* ####Implement a proxy system for stock checking to prevent IP ban for actual purchase
* ####Add Unit Tests
* ####Improve Logging
* ####General bug fixes and extensive beta testing
* ####Add code docstrings, type hinting, and comments
* ####Find workaround for having to refresh the page to click the checkout button, or select address and payment fields during guest checkout