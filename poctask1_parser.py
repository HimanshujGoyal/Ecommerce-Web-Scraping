import os
import csv, json
from bs4 import BeautifulSoup, Tag


def poc1Parser():
    '''
    To parse the html document I have used Beautifulsoup library and used objects like Tag, Navigable string to parse complex tree,
    and returned data in the form of dictionary
    dictionary structure
    data_collected = {
        'unique_key': {
            'product_url': product_url_clean,
            'product_name': product_name,
            'product_rating': product_rating,
            'actual_price': actual_price,
            'discount_price': discount_price
        }
    }
    '''
    data_collected = {}

    html_files = os.listdir('cdiscount_htmlbody') #root folder where all html bodydumps are present

    file_count = 1
    for file in html_files: #itertate over all the file in folder endswith ".html"
        if file.endswith(".html"):
            with open(f'cdiscount_htmlbody\{file}', 'rb') as file:
                soup = BeautifulSoup(file, 'html.parser') #soup object of beautifulsoup class and html parser
                # print(soup)

                product_grid = soup.find('ul', class_="lpGrid")
                
                product_count = 1
                for li in product_grid:
                    if isinstance(li, Tag):
                        try:
                            product_url = li.a.get('href')
                            if product_url == "#":
                                pass
                            else:
                                product_url_clean = product_url
                            
                            product_name = li.find('div', class_="prdtBTit").span.text
                            product_rating = li.find('div', class_="prdtBStar").span.text
                            # print(product_name.strip())
                            try:
                                actual_price = li.find('div', class_="priceLine").find('span', class_="hideFromPro").text
                                actual_price = actual_price.split("€")[0]
                                discount_price = li.find('div', class_="strikedPriceZone").find('span', class_="hideFromPro").text
                                discount_price = discount_price.split("€")[0]
                            except:
                                actual_price = li.find('div', class_="priceLine").find('span', class_="hideFromPro").text
                                actual_price = actual_price.split("€")[0]
                                discount_price = "n/a"

                        except AttributeError:
                            pass

                        unique_key = str(file_count)+"_"+str(product_count)   
                        # print(unique_key,product_url_clean,product_name, product_rating,actual_price, discount_price)

                        data_collected[unique_key] = {
                            'product_url': product_url_clean,
                            'product_name': product_name,
                            'product_rating': product_rating,
                            'actual_price': actual_price,
                            'discount_price': discount_price
                        }

                        product_count += 1

        file_count += 1

    return data_collected
            
def write_csv():
    '''
    function that will write CSV file from the dictinory returned by poc1Parser() function. 
    '''
    data = poc1Parser()

    try:
        with open("cdiscount_poc1_output.csv", "w", newline="",encoding="utf-8") as output_file:
            print("File opened")
            fieldname = ['product_url', 'product_name', 'product_rating', 'actual_price', 'discount_price']

            writter = csv.DictWriter(output_file, fieldnames=fieldname, delimiter=",")

            if output_file.tell() == 0:
                writter.writeheader()

                for i in data:
                    writter.writerow({
                        'product_url': data[i]['product_url'],
                        'product_name': data[i]['product_name'],
                        'product_rating': data[i]['product_rating'],
                        'actual_price': data[i]['actual_price'],
                        'discount_price': data[i]['discount_price']
                    })

            print("Output file generated")
                    
    except Exception as e:
        print("Exception occured while writing the file")


def main():
    print("[+] Parsing started")
    # print(len(poc1Parser()))
    write_csv()

if __name__ == "__main__":
    main()