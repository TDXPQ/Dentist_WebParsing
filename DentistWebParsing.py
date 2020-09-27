# Title: DentisWebParsing     Author: TDXPQ (Aditya Jindal)
# Description:  Script to scrape dentist's information from yellow pages.

# Import needed python libraries.
import urllib.request

# Import needed exteranl libraries.
import bs4 as bs
import pandas as pd

class Dentist:      #Used object to organize parsed data easier.
    def __init__(self, name, phone_number, street_address, town_name, zip_code):
        self.name = name;
        self.phone_number = phone_number;
        self.street_address = street_address;
        self.town_name = town_name;
        self.zip_code = zip_code;


def dentist_info_scrape(url, max_page):      #Get dentist information and put all of them in a list.
    dentists = []

    for page in range(1, (max_page+1)):
        print(page)
        if page == 1:       #Usually the first url in a series of urls has a slighlty different url layout.
            dentist_sause = urllib.request.urlopen(url).read()
        else:
            dentist_sause = urllib.request.urlopen(url + '?page='+str(page)).read()

        dentist_soup = bs.BeautifulSoup(dentist_sause, 'lxml')

        for div in dentist_soup.find_all(class_= 'v-card'):     #Sort the website html to isolate the virtual business cards for the dentists on each page.
            try:                                                #Used a try loop because some div are empty and do not contain all the information causing an error in the code.
                #Propogate all the neccessary information into temporary varaibles
                name = div.find('span').text
                phone_number = div.find(class_= 'phones phone primary').text
                street_address = div.find(class_= 'street-address').text
                town_name = div.find(class_= 'locality').text[:-10]
                zip_code = div.find(class_= 'locality').text[-5:]

                dentists.append(Dentist(name, phone_number, street_address, town_name, zip_code))
            except:
                pass

    return dentists


def create_zip_list(url):       #Function to make sure all the dentists are in a a designated county.
    zip_sauce = urllib.request.urlopen(url).read()
    zip_soup = bs.BeautifulSoup(zip_sauce, 'lxml')

    zip_codes = []

    for div in zip_soup.find_all(class_= 'col-md-4'):
        for zips in div.find_all('u'):
            zip_codes.append(zips.text[:5])

    return zip_codes        #Return a list of all the zip codes to compare against.


def dentist_zip_check(dentists, zip_codes):        #Check dentist zip code to make sure it is within a certain group of zip codes.
    new_list = []
    for dentist in dentists:
        if dentist.zip_code in zip_codes:
            new_list.append(dentist)

    return new_list     # Return a new list of objects that fit the zip code requirements.


def display_excel(dentists, col, document_name):        # Function used to create pandas data frame to easily export the data to various file formats.
    # Create a 2d array to pass into pandas when creating the data frame.
    dentists_list = []
    for dentist in dentists:
        dentists_list.append([dentist.name, dentist.phone_number, dentist.street_address, dentist.town_name, dentist.zip_code])

    df = pd.DataFrame(dentists_list, columns=col)       # Create data frame.
    df.to_excel(rf'{document_name}.xlsx', index=False)  # Export to excel, this line can be changed to export to any file type pandas supports.

    return


def main():
    # Define hard coded variables.
    dentist_yellow_page_url = 'https://www.yellowpages.com/long-island-ny/dentists'
    max_page  = 62
    zip_code_page_url = 'https://www.bestplaces.net/find/zip.aspx?county=36103&st=NY'
    columns = ['Name', 'Phone Number', 'Street Address', 'Town Name', 'Zip Code']
    document_name = 'Dentist'

    dentists = dentist_info_scrape(dentist_yellow_page_url, max_page)
    zip_codes = create_zip_list(zip_code_page_url)
    dentists = dentist_zip_check(dentists, zip_codes)
    display_excel(dentists, columns, document_name)

    return

if __name__ == '__main__':
    main()