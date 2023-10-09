import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class CommerceTest(unittest.TestCase):
    
    USERNAME = "standard_user"
    LOCKEDUSERNAME = "locked_out_user"
    GLITCHUSERNAME = "performance_glitch_user"
    PASSWORD = "secret_sauce"
    
    driver = None
    wait = None
    actions = None
    
    def set_up(self, url):
        dimension = (1920, 1080)
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(4)  # seconds
        self.driver.set_window_size(*dimension)
        self.wait = WebDriverWait(self.driver, 10)  # seconds
        self.driver.get(url)

        self.actions = ActionChains(self.driver)
    
    def log_in(self, name, password):
        self.driver.find_element(By.ID, "user-name").send_keys(name)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

        elements = self.driver.find_elements(By.ID, "inventory_container")
        assert len(elements) > 0

    def log_out(self):
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        self.driver.find_element(By.ID, "logout_sidebar_link").click()

        elements = self.driver.find_elements(By.CLASS_NAME, "login_container")
        assert len(elements) > 0
        
    def tearDown(self):
        self.log_out()
        self.driver.quit()

    def test_commerce(self):

        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.ID, "shopping_cart_container").click()

        cart_page_element = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_list")))
        cart_item_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self.assertEqual(cart_item_name, "Sauce Labs Backpack")

        self.driver.find_element(By.ID, "checkout").click()
        checkout_page_element = self.wait.until(EC.visibility_of_element_located((By.ID, "checkout_info_container")))

        self.driver.find_element(By.ID, "first-name").send_keys("John")
        self.driver.find_element(By.ID, "last-name").send_keys("Doe")
        self.driver.find_element(By.ID, "postal-code").send_keys("10001")
        self.driver.find_element(By.ID, "continue").click()

        checkout_item_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self.assertEqual(checkout_item_name, "Sauce Labs Backpack")

        self.driver.find_element(By.ID, "finish").click()
        success_is_displayed = self.driver.find_element(By.ID, "checkout_complete_container").is_displayed()
        self.assertTrue(success_is_displayed)

        self.tearDown()
        
        
    def test_assert_item_name_on_item_info_page(self):
        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        # go to the item
        self.driver.find_element(By.ID, "item_4_title_link").click()

        # Check that texts exist on the site
        # Sauce Labs Backpack
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "inventory_details_name").text, "Sauce Labs Backpack")
        
        expected_desc = "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "inventory_details_desc").text, expected_desc)
        
        self.tearDown()

    def test_move_to_linkedin(self):
        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        # Scroll down
        self.actions.move_to_element(self.driver.find_element(By.CLASS_NAME, "social_linkedin")).perform()

        # Go to Linkedin page
        self.driver.find_element(By.CLASS_NAME, "social_linkedin").click()

        # Verify you are on the Linkedin page
        tab_list = self.driver.window_handles
        self.driver.switch_to.window(tab_list[1])

        self.assertEqual(self.driver.current_url, "https://www.linkedin.com/company/sauce-labs/")
        self.driver.close()
        self.driver.switch_to.window(tab_list[0])

        self.tearDown()    
        
    def test_assert_sorting(self):
        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        # Click the filters box
        self.driver.find_element(By.CLASS_NAME, "select_container").click()
        # click Z-A
        self.driver.find_element(By.CSS_SELECTOR, "option[value='za']").click()
        # check that the name at the top is "Test.allTheThings() T-Shirt (Red)
        self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text, "Test.allTheThings() T-Shirt (Red)")

        # click the filters box
        self.driver.find_element(By.CLASS_NAME, "select_container").click()
        # click A-Z 
        self.driver.find_element(By.CSS_SELECTOR, "option[value='az']").click()
        # check that the name at the top is "Sauce Labs Backpack"
        self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text, "Sauce Labs Backpack")

        # click the filters box
        self.driver.find_element(By.CLASS_NAME, "select_container").click()
        # click low-High
        self.driver.find_element(By.CSS_SELECTOR, "option[value='hilo']").click()
        # check that the name at the top is "Sauce Labs Onesie"
        self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text, "Sauce Labs Fleece Jacket")

        # click the filters box
        self.driver.find_element(By.CLASS_NAME, "select_container").click()
        # click high-Low
        self.driver.find_element(By.CSS_SELECTOR, "option[value='lohi']").click()
        # check that the name at the top is "Sauce Labs Fleece Jacket"
        self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text, "Sauce Labs Onesie")
        self.tearDown()

    def test_assert_shopping_button_states(self):
        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        # Click all add-to-cart buttons
        buttons_add = self.driver.find_elements(By.CSS_SELECTOR, "[id^=add-to-cart]")
        for button in buttons_add:
            self.actions.move_to_element(button).perform()
            button.click()

        # check that the cart button says 6
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text, "6")

        # Click all remove buttons
        buttons_remove = self.driver.find_elements(By.CSS_SELECTOR, "[id^=remove]")
        for button in buttons_remove:
            self.actions.move_to_element(button).perform()
            button.click()

        # check that the cart button says nothing
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")) < 1)
        self.tearDown()

    def test_assert_user_log_in_cache_permanency(self):
        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)
        
        # Add items to cart
        self.actions.move_to_element(self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")).perform()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        self.actions.move_to_element(self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light")).perform()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

        self.log_out()
        # Check that items are still in the cart
        self.log_in(self.USERNAME, self.PASSWORD)

        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text, "2")    
        self.tearDown()

    def test_assert_app_reset_functionality(self):  # flaky test
        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        # Select all items
        buttons_add = self.driver.find_elements(By.CSS_SELECTOR, "[id^=add-to-cart]")
        for button in buttons_add:
            self.actions.move_to_element(button).perform()
            button.click()

        # Click on sidebar
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        # Click on Reset App State
        self.driver.find_element(By.ID, "reset_sidebar_link").click()
        self.driver.find_element(By.ID, "react-burger-cross-btn").click()

        # Check that the app reset but that there is a bug with "Remove" still staying instead of resetting to Add Cart
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")) < 1)

        self.assertTrue(self.driver.find_element(By.ID, "remove-sauce-labs-backpack").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "remove-sauce-labs-bike-light").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "remove-sauce-labs-bolt-t-shirt").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "remove-sauce-labs-fleece-jacket").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "remove-sauce-labs-onesie").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "remove-test.allthethings()-t-shirt-(red)").is_displayed())

        self.driver.find_element(By.ID, "react-burger-cross-btn").click()
        self.tearDown()
    
    def test_assert_error_accessing_without_log_in(self):
        self.set_up("https://www.saucedemo.com/cart.html")  # Direct link provided here

        # Assert that the error is the correct one
        expected_error = "Epic sadface: You can only access '/cart.html' when you are logged in."
        self.assertEqual(expected_error, self.driver.find_element(By.CLASS_NAME, "error-message-container").text)

        self.log_in(self.USERNAME, self.PASSWORD)

        # Now try logging in and then jumping to a link
        self.driver.get("https://www.saucedemo.com/cart.html")

        # Assert that it worked when you were logged in
        self.assertTrue(self.driver.find_element(By.ID, "cart_contents_container").is_displayed())
        self.tearDown()

    def test_assert_locked_out_user(self):
        self.set_up("https://www.saucedemo.com")

        # Attempt to log in with locked out user
        self.driver.find_element(By.ID, "user-name").send_keys(self.LOCKEDUSERNAME)
        self.driver.find_element(By.ID, "password").send_keys(self.PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()

        # Clear the input fields
        self.driver.find_element(By.ID, "user-name").send_keys(Keys.CONTROL + "a", Keys.BACK_SPACE)
        self.driver.find_element(By.ID, "password").send_keys(Keys.CONTROL + "a", Keys.BACK_SPACE)

        # Assert the error
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        actual_error = self.driver.find_element(By.CLASS_NAME, "error-message-container").text
        self.assertEqual(expected_error, actual_error)

        # Attempt to log in with the normal user
        self.log_in(self.USERNAME, self.PASSWORD)
        
        self.tearDown()
        
        
        
    def Glitched_User_Experience(self):

        self.set_up("https://www.saucedemo.com")
        self.log_in(self.USERNAME, self.PASSWORD)

        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.ID, "shopping_cart_container").click()

        cart_page_element = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_list")))
        cart_item_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self.assertEqual(cart_item_name, "Sauce Labs Backpack")

        self.driver.find_element(By.ID, "checkout").click()
        checkout_page_element = self.wait.until(EC.visibility_of_element_located((By.ID, "checkout_info_container")))

        self.driver.find_element(By.ID, "first-name").send_keys("John")
        self.driver.find_element(By.ID, "last-name").send_keys("Doe")
        self.driver.find_element(By.ID, "postal-code").send_keys("10001")
        self.driver.find_element(By.ID, "continue").click()

        checkout_item_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self.assertEqual(checkout_item_name, "Sauce Labs Backpack")

        self.driver.find_element(By.ID, "finish").click()
        success_is_displayed = self.driver.find_element(By.ID, "checkout_complete_container").is_displayed()
        self.assertTrue(success_is_displayed)

        self.tearDown()

if __name__ == "__main__":
    unittest.main()
