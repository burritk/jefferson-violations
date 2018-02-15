from pyscraper.selenium_utils import get_headed_driver, wait_for_classname, wait_for_id
from pyscraper.data_dump_file import DataFile

driver = get_headed_driver()
try:
    driver.get("http://jp-appserver.jeffparish.net/servicerequest/findServices.aspx")
    links = driver.find_elements_by_tag_name('a')
    address = [link for link in links if 'Address' in link.text][0]
    address.click()
    output = DataFile('violations')
    with output:
        for index in range(10,40):
            street = wait_for_id(driver, 'ddlStreet')
            options = street.find_elements_by_tag_name('option')
            options[index].click()
            search_button = driver.find_element_by_id('btnSearch')
            search_button.click()
            rows = driver.find_elements_by_tag_name('tr')

            for i in range(len(rows)):
                rows = driver.find_elements_by_tag_name('tr')
                row = rows[i]
                test_text = [element.text for element in row.find_elements_by_tag_name('tr')]
                row_text = row.text
                first_section = row_text.split()
                if 'repeat offender' in row_text.lower() and ('/2018' in row_text.lower() or '/2017' in row_text):
                    print row_text
                    link = row.find_element_by_tag_name('a')
                    link.click()
                    wait_for_classname(driver, 'lbl_title')
                    second_section = [element.text for element in driver.find_elements_by_class_name('lbl_title')]

                    service_id = first_section[0]
                    item_number = first_section[1]
                    type = first_section[2] + " " + first_section[3]
                    location = first_section[4] + " " + first_section[5] + " " + first_section[6] + " " + first_section[7]
                    service_requested = first_section[8]

                    output.load_values(service_id, item_number, type, location, service_requested)

                    complaint_type = second_section[5]
                    complaint_dept = second_section[7]
                    received_date = second_section[9]
                    subdivision = second_section[11]
                    address = second_section[13]
                    city = second_section[15]
                    bank_of_river = second_section[17]

                    output.load_values(complaint_type, complaint_dept, received_date, subdivision, address, city, bank_of_river)

                    activity_table = driver.find_element_by_class_name('special_table')
                    table_rows = activity_table.text.split('\n')
                    activity_information = []
                    for trow in table_rows[1:]:
                        type_of_activity = ''
                        for word in trow.split()[:-1]:
                            type_of_activity += word + " "
                        date_of_activity = trow.split()[-1]
                        type_of_activity = type_of_activity.strip()
                        activity_information.append((type_of_activity, date_of_activity))

                    for activity in activity_information:
                        type_of_activity, date_of_activity = activity

                        output.load_values(type_of_activity, date_of_activity)

                    output.write_loaded()
                    driver.back()
                else:
                    continue
            driver.back()
finally:
    driver.close()

print len(rows)
print 'h'