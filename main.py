from pyscraper.selenium_utils import get_headed_driver, get_headless_driver, wait_for_classname, wait_for_id
from pyscraper.data_dump_file import DataFile

driver = get_headless_driver(no_sandbox=True)
try:
    driver.get("http://jp-appserver.jeffparish.net/servicerequest/findServices.aspx")
    links = driver.find_elements_by_tag_name('a')
    address = [link for link in links if 'Address' in link.text][0]
    address.click()

    street = wait_for_id(driver, 'ddlStreet')
    options = street.find_elements_by_tag_name('option')

    output = DataFile('violations5')
    log = DataFile('log5')
    with output, log:
        for index in range(2, len(options)):
            street = wait_for_id(driver, 'ddlStreet')
            options = street.find_elements_by_tag_name('option')
            options[index].click()
            street = options[index].text
            search_button = driver.find_element_by_id('btnSearch')
            search_button.click()
            rows = driver.find_elements_by_tag_name('tr')
            log.load_value(street + " rows: " + str(len(rows)))
            repeat_offenders = 0
            print '\n' + street, len(rows)
            for i in range(len(rows)):
                print i,
                rows = driver.find_elements_by_tag_name('tr')
                row = rows[i]
                test_text = [element.text for element in row.find_elements_by_tag_name('tr')]
                row_text = row.text
                first_section = row_text.split()
                if 'repeat offender' in row_text.lower() and ('/2018' in row_text or '/2017' in row_text):
                    repeat_offenders += 1
                    print '\n' + row_text
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
                    # log.write_values(street, len(table_rows))
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
            log.load_value(str(repeat_offenders))
            log.write_loaded()
            driver.back()
finally:
    driver.close()

print len(rows)
print 'h'