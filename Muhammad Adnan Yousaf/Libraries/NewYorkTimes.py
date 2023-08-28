from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP


class NewYorkTimes:

    def __init__(self):
        self.browser = Selenium()

        self.searh_phrase = "industry"
        self.news_sections = ["Arts", "Books"]
        self.number_of_months = 0

        self.search_results_data = {
            "title": [],
            "description": [],	
            "date": [],
            "picture filename": []
        }

        self.sort_by = "newest"

        self.terms_dialogue_selector = "css:#complianceOverlay > div > button"
        self.search_icon_selector = "css:#app > div:nth-child(4) > div.NYTAppHideMasthead.css-1r6wvpq.e1m0pzr40 > header > section.css-9kr9i3.e1m0pzr42 > div.css-qo6pn.ea180rp0 > div.css-10488qs > button"
        self.search_input_box_selector = "css:#search-input > form > div > input"
        self.sort_by_selector = "css:#site-content > div > div.css-1npexfx > div.css-nhmgdh > form > div.css-hrdzfd > div > select"
        self.sections_button_selector = "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > button"
        self.news_sections_selector = {
            "Any": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(1) > label > input[type=checkbox]",
            "Arts": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(2) > label > input[type=checkbox]",
            "Books": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(3) > label > input[type=checkbox]",
            "Business": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(4) > label > input[type=checkbox]",
            "New York": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(5) > label > input[type=checkbox]",
            "Opinion": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(6) > label > input[type=checkbox]",
            "Style": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(7) > label > input[type=checkbox]",
            "Technology": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(8) > label > input[type=checkbox]",
            "U.S.": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(9) > label > input[type=checkbox]",
            "World": "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div:nth-child(2) > div > div > div > ul > li:nth-child(10) > label > input[type=checkbox]",
        }
        self.date_range_button_selector = "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div.css-wsup08 > div > div > button"
        self.specific_date_range_selector = "css:#site-content > div > div.css-1npexfx > div.css-1az02az > div > div > div.css-wsup08 > div > div > div > ul > li:nth-child(6) > button"
        self.start_date_input_selector = "css:#startDate"
        self.end_date_input_selector = "css:#endDate"

    
    def open_website_and_search(self):
        self.browser.open_chrome_browser("https://www.nytimes.com/", maximized=True, headless=False)
        self.browser.click_element_if_visible(self.terms_dialogue_selector)
        # self.browser.click_button(self.terms_dialogue_selector)
        self.browser.click_button(self.search_icon_selector)
        self.browser.input_text(self.search_input_box_selector, self.searh_phrase)
        self.browser.press_keys(self.search_input_box_selector, "ENTER")


    def sort_by_newest(self):
        self.browser.select_from_list_by_value(self.sort_by_selector, self.sort_by)


    def select_news_sections(self):
        self.browser.click_button(self.sections_button_selector)
        if "Any" in self.news_sections:
            self.browser.select_checkbox(self.news_sections_selector["Any"])
        else:
            for news_section in self.news_sections:     
                self.browser.select_checkbox(self.news_sections_selector[news_section])
        self.browser.click_button(self.sections_button_selector)
        

    def select_date_range(self):
        self.browser.click_button(self.date_range_button_selector)
        self.browser.click_button(self.specific_date_range_selector)
        self.browser.input_text(self.start_date_input_selector, "08/01/2023")
        self.browser.press_keys(self.start_date_input_selector, "ENTER")
        self.browser.input_text(self.end_date_input_selector, "08/20/2023")
        self.browser.press_keys(self.end_date_input_selector, "ENTER")

    
    def extract_searched_results(self):
        search_results = self.browser.find_elements('css:li.css-1l4w6pd')
        for result in search_results:
            try:
                _title = self.browser.get_text(self.browser.get_webelement("css:h4.css-2fgx4k", result))
                _description = self.browser.get_text(self.browser.get_webelement("css:p.css-16nhkrn", result))
                _date = self.browser.get_text(self.browser.get_webelement("css:span.css-17ubb9w", result))
                _image_url = self.browser.get_element_attribute(self.browser.get_webelement("css:img.css-rq4mmj", result), "src")
                _image_file_name = _image_url.split("?")[0].split("/")[-1]
                HTTP().download(url=_image_url, target_file=f"./output/images/{_image_file_name}", overwrite=True)
                
                self.search_results_data["title"].append(_title)
                self.search_results_data["description"].append(_description)
                self.search_results_data["date"].append(_date)
                self.search_results_data["picture filename"].append(_image_file_name)
                
                print("\n", _date, "\n", _title, "\n", _description, "\n", _image_url, "\n", _image_file_name, "\n")
            except Exception as e:
                print(f"Exception: {e}")


    def save_search_results_data(self):
        lib = Files()
        try:
            lib.open_workbook("./output/Search_Results.xlsx")
        except:
            lib.create_workbook(path="./output/Search_Results.xlsx", sheet_name="Sheet1")
        lib.read_worksheet("Sheet1")
        lib.append_rows_to_worksheet(self.search_results_data)
        lib.save_workbook()


    def close_all(self):
        self.browser.close_all_browsers()
