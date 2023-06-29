from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta
import time

# This function generates a list of dates between two dates.
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# This line sets the path to the ChromeDriver executable and the url for the website we want to scrape.
PATH = "C:\Program Files (x86)\chromedriver.exe"
url = 'https://midrug.safenet.co.il/app/'

# This line creates a new instance of the ChromeDriver object.
driver = webdriver.Chrome(PATH)

# This line opens the Midrug website.
driver.get(url)

# This line defines the start and end dates for the data scraping.
start_date = date(2020, 1, 1)
end_date = date(2023, 5, 22)

# This line creates an empty list to store the data.
lst = []

# This loop iterates over the dates between the start and end dates.
for single_date in daterange(start_date, end_date):

    # This line selects the "1" crowd from the dropdown menu.
    crowd = Select(driver.find_element(By.ID, 'Crowd'))
    crowd.select_by_value('1')

    # This line clears the text input field for the date.
    date = driver.find_element(By.ID, 'TheDate')
    date.clear()

    # This line enters the date into the text input field.
    date.send_keys(single_date.strftime(r"%d%m%Y"))

    # This line clicks the search button.
    search = driver.find_element(By.XPATH, '//*[@id="DataPlus"]/table/tbody/tr[6]/td[2]/input')
    search.click()

    # This line tries to find the table with the ratings data.
    try:
        time.sleep(0.5)
        table = driver.find_element(By.ID, "Rep2")

    # This line catches the `NoSuchElementException` exception and sets the table to `None`.
    except NoSuchElementException:
        table = None
        pass

    # This line only adds the data to the list if the table exists.
    if table is not None:
        data = pd.read_html(table.get_attribute("outerHTML"), encoding='windows-1255')[0]
        data_lst = data.values.tolist()
        for row in data_lst:
            lst.append(row)

# This line creates a Pandas DataFrame from the list of data.
df = pd.DataFrame(lst, columns=data.columns)

# This line writes the DataFrame to a CSV file.
df.to_csv('text.csv', encoding='windows-1255')

# This line prints the first five rows of the DataFrame.
print(df.head())

# This line quits the ChromeDriver object.
driver.quit()