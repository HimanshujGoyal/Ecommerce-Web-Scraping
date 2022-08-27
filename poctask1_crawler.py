import os
import requests
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
from dotenv import load_dotenv

'''
While performing basic research and analysis on cdiscount site I have noticed that after pasing the request to URL, I was getting 202 Accepted response,
as the issue was to bypass the captcha that I was getting before loading the product page URL, while checking the cookies and headers used by the
site I noticed that the captcha key is being passed from the cookies to resolve hcaptcha issue.
for solving the hcaptcha I have made us of two captcha service. 
when the site response is 202 (captcha page) I have parse the data-sitekey of hcaptcha and pass the site in two captcha solve object along with base
url to get the captcha key, this captcha key I have passed in cookies parameter for further request.
'''
def solveCaptcha():
    '''
    Function uses Two captcha server to return the captcha key which further we can pass in 
    cookie parameter to resolve captcha issue with python requests.

    result = solver.hcaptcha(sitekey=data_sitekey, url=url)
    in the above object we can pass sitekey of hcaptcha and URL which returns the string of captcha solve key.
    '''
    try:
        load_dotenv()
        api_key=os.environ.get('2CAPTCHA_APIKEY')
    except KeyError:
        print("Please define the environment variable 2CAPTCHA_APIKEY")

    solver = TwoCaptcha(api_key)

    url = 'https://www.cdiscount.com/bricolage/climatisation/traitement-de-l-air/ioniseur/l-166130303.html'

    headers = {
        'authority': 'www.cdiscount.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"fh_713315c92c144108fa6a3b74cdafa2b347a8436b"',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/536.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/536.36',
    }

    proxy = {
    "http": "http://50.253.49.189:54321"
    }

    response = requests.get(url, headers=headers, proxies=proxy)

    if response.status_code == 202:
        #Response code is Accepted as the task is to solve captcha issue

        soup = BeautifulSoup(response.content, "html.parser")

        h_captcha_tag = soup.find('div', class_="g-recaptcha")
        data_sitekey = h_captcha_tag.attrs.get('data-sitekey')
        print(data_sitekey)

        result = solver.hcaptcha(sitekey=data_sitekey, url=url)
        print(result)

        captcha_value = result.get('code')

        cookies = {
            'captcha': captcha_value
        }
    else:
        print("Error while handling captcha")

    return cookies


def cdiscount():
    cookies = solveCaptcha()

    headers = {
        'authority': 'www.cdiscount.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"fh_713315c92c144108fa6a3b74cdafa2b347a8436b"',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/536.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/536.36',
    }

    #free ninja proxy
    proxy = {
    "http": "http://50.253.49.189:54321"
    }

    response = requests.get('https://www.cdiscount.com/bricolage/climatisation/traitement-de-l-air/ioniseur/l-166130303.html', cookies=cookies, headers=headers, proxies=proxy)

    res_status = response.status_code
    if res_status == 200:
        num_of_pages = [] #list of product listing page

        with open('cdiscount_htmlbody/cdiscount_listingpage_1.html', 'rb') as file:
            file.write(response.content)
            print("HTML body collected..")

            soup = BeautifulSoup(file, 'html.parser')

            pagination = soup.find('ul', id='PaginationForm_ul')

            try:
                for li in pagination.find_all('li'):
                    if li.a.get('href') is not None:
                        num_of_pages.append(li.a.get('href'))
            except AttributeError:
                print("anchor tag not found")

        for page in num_of_pages[:1]:
            base_url = "https://www.cdiscount.com"
            pagination_url = base_url+page+"#_his_"
            print(pagination_url)
            page_no = pagination_url.split('.html')[0].split('-')[-1]

            response = requests.get(pagination_url, cookies=cookies, headers=headers, proxies=proxy)

            if response.status_code == 200:
                with open(f'cdiscount_htmlbody/cdiscount_listingpage_{page_no}.html', 'wb') as file:
                    file.write(response.content)

                    print("HTML body collected for page number: ", page_no)
            else:
                print(response.content)
                print("Error code: ", response.status_code)
    else:
        print("Error", res_status)


def main():
    print("[+] Started Crawler..")
    cdiscount()
    # cookies = solveCaptcha()
    # print(cookies)


if __name__ == "__main__":
    main()
