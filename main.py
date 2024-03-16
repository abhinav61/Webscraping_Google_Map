from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse

# Contain data of each Business
@dataclass    # it provides more features along the way
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    # reviews: int = None

# Contain the list of Businesses
@dataclass
class BusinessList:
    business_list1: list[Business] = field(default_factory=None)

    def dataframe(self):
    # convert business list to the data frame
        return pd.json_normalize((asdict(business) for business in self.business_list1), sep = "") 
    
    def save_to_excel(self,filename):
        self.dataframe().to_excel(f'{filename}.xlsx', index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f'{filename}.csv', index=False)

def main():
    # call the playwright to open the browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto('https://www.google.com/maps', timeout= 60000)
        page.wait_for_timeout(5000) #sleep for 5 seconds

        # id is taken from the web console and locator swill serach for that in the web
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press('Enter')
        page.wait_for_timeout(5000)

        #fetching and counting all the list 
        Listings = page.locator('//div[@role="main"]').all()
        print(len(Listings))

        business_list1 = BusinessList

        for listing in Listings[:20]:
            listing.click()
            page.wait_for_timeout(5000)

            name_path = '//h1[contains(@class, "fontHeadLineLarge")]/span[2]'
            address_path = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_path = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_path = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            # review_count_path = '//button[@jsaction="pane.reviewChart.moreReviews"]//span'

            business = Business()
            business.name = page.locator(name_path).inner_text()
            business.address = page.locator(address_path).inner_text()
            business.website = page.locator(website_path).inner_text()
            business.phone_number = page.locator(phone_number_path).inner_text()
            # business.reviews = page.locator(review_count_path).inner_text()

            business_list1 = business_list1.append(business)

            #Save the data
            business_list1.save_to_excel('google_maps_data_excel')
            business_list1.save_to_csv('google_maps_data_csv')

        browser.close()

    
if __name__ == "__main__":
    # this code will give a way to enter arguments in command line to passed on to python
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-l", "--location", type=str)
    args = parser.parse_args()

    if args.search and args.location:
    # it will serach the loaction and and location
        search_for = f'{args.search}  {args.location}'
    else:
        search_for = 'Hotel Jamshedpur'

    main()