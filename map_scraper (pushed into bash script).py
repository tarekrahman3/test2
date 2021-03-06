from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import re

URL = input("Enter Google Map URL: ")
try:
	URL = URL.replace('?hl=en', '')
except:
	pass
keyword = re.search('\/maps\/search\/(.+)\/@', URL).group(1).replace('+',' ')
city = re.search('\!2s(.+?)\,', URL).group(1).replace('+', ' ')
Export_File_Name = f"{city} - {keyword}"

options = Options()
options.add_argument("--no-sandbox")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument('--ignore-certificate-errors')
driver=webdriver.Chrome(options=options, executable_path='/home/tarek/MY_PROJECTS/Selenium_Projects/webdrivers/chromedriver')

dict_array = []

def headers_loop():
	try:
		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@jsaction, 'mouseover:pane')]/a")))
	except:
		pass
	for i in range(20):
		try:
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@jsaction, 'mouseover:pane')]/a")))
		except:
			pass
		current_results_ = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
		c_number = len(current_results_)
		we_need = i
		if i>=c_number:
			while True:
				try:
					r = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
					action = ActionChains(driver)
					action.move_to_element(r[(len(r))-1]).perform()
					r[(len(r))-1].location_once_scrolled_into_view		
					if (len(r))>i:
						break
					else:
						pass		
				except:
					pass		
		else:
			pass
		results = driver.find_elements_by_xpath("//div[contains(@jsaction, 'mouseover:pane')]")
		c_time = time.ctime()
		try:
			rate = results[i].find_element_by_xpath(".//span[contains(@class, 'rating-score')]").text
		except:
			rate = ''
		try:
			ratings = results[i].find_element_by_xpath(".//div[contains(@class, 'rating-container')]/span[2]//span[@role='img']").get_attribute('aria-label')
		except:
			ratings = ''
		try:
			details = results[i].find_element_by_xpath(".//div[contains(@class, 'info-line')]/span/jsl").text
		except:
			details = ''
		try:
			location=results[i].find_element_by_xpath(".//span[contains(@class, 'result-location')]").text
		except:
			location = ''
		rs = driver.find_elements_by_xpath("//div[contains(@jsaction, 'mouseover:pane')]/a")
		action = ActionChains(driver)
		rs[i-1].location_once_scrolled_into_view
		action.move_to_element(rs[i]).click().perform()	
		
		try:
			wait_for_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "section-hero-header-title")]')))
		except:
			rs = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
			action = ActionChains(driver)
			action.move_to_element(rs[i]).perform()	
			rs[i-1].location_once_scrolled_into_view
			rs[i].click()
			wait_for_title = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "section-hero-header-title")]')))
		
		business_url = f"{c_time} | {str(driver.current_url)}"
		title = driver.find_element_by_xpath(".//h1[contains(@class, 'section-hero-header')]").text
		try:
			address = driver.find_element_by_xpath('//button[contains(@data-item-id, "address")]').get_attribute('aria-label')
		except:
			address = ''
		try:
			website = driver.find_element_by_xpath("//button[contains(@aria-label, 'Website:')]").get_attribute('aria-label')
		except:
			website = ''
		try:
			phones = driver.find_element_by_xpath("//button[contains(@aria-label, 'Phone:')]").get_attribute('aria-label')
		except:
			phones = ''
		print(f" >  {str((len(dict_array)+1))}   -    '{title}'")
		print(f"               {address}")
		dict_array.append({
		'business_url': business_url,
		'title': title,
		'rate': rate,
		'ratings': ratings,
		'details': details,
		'location': location,
		'phones': phones,
		'website': website,
		'address': address,
		'city': city,
		'keyword': keyword
		})
		try:
			back_to_list=driver.find_element_by_xpath('//button[contains(@class, "section-back")]')
		except:
			back_to_list=driver.find_element_by_xpath('//button[@class="searchbox-button"]')
		
		back_to_list.click()
		time.sleep(1)
		try:
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@jsaction, 'mouseover:pane')]")))
		except:
			pass

def next_pagination():
	try:
		next_page=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="n7lv7yjyC35__section-pagination-button-next"]')))
		next_page.click()
	except:
		time.sleep(10)
		next_page.click()
	time.sleep(4)

def write_csv():
	csvtime = time.ctime()
	file_name=f"{csvtime} - {str(Export_File_Name)}.csv"
	fields = list(dict_array[0].keys())
	with open(file_name, 'w') as csvfile: 
		writer = csv.DictWriter(csvfile, fieldnames = fields)
		writer.writeheader()
		writer.writerows(dict_array)
	print(f"new file created: {file_name}")

def main():
	try:
		driver.get(str(URL) + '?hl=en')
		try:
			while True:
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "route-preview-controls")]//input[contains(@class, "checkbox-input")]')))
				preview = driver.find_element_by_xpath('//div[contains(@class, "route-preview-controls")]//input[contains(@class, "checkbox-input")]')
				preview.click()
				if (preview.get_attribute('aria-checked'))=='false':
					break
				else:
					pass
		except:
			pass
		while True:
			headers_loop()
			if len(dict_array)>199:
				break
			else:
				pass
			next_pagination()
	finally:
		write_csv()
		driver.quit()
main()
print('############  Sequence Completed  ############')
