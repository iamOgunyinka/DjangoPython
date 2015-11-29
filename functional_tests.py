from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest( unittest.TestCase ):
    
    def check_for_row_in_list_table( self, row_text ):
        table = self.browser.find_element_by_id( 'id_list_table' )
        rows = table.find_elements_by_tag_name( 'tr' )
        my_list = [ row.text for row in rows ]
        self.assertIn( row_text, my_list )


    def send_input( self, text, duration ):
        input_box = self.browser.find_element_by_id( 'id_new_item' )
        self.assertEqual( input_box.get_attribute( 'placeholder' ), 'Enter a to-do item' )
        input_box.send_keys( text )
        input_box.send_keys( Keys.ENTER )
        time.sleep( duration )


    def setUp( self ):
        self.browser = wb.Chrome( 'C:\Downloads\chromedriver' )


    def tearDown( self ):
        self.browser.quit()


    def test_can_start_a_list_and_retrieve_it_later( self ):
        self.browser.get( 'http://127.0.0.1:8000' )
        self.assertIn( 'To-Do', self.browser.title )
        header_text = self.browser.find_element_by_tag_name( 'h1' ).text
        self.assertIn( 'To-Do', header_text )

        self.send_input( 'Buy peacock feathers', 4 )
        self.send_input( 'Peacock can fly in the sky', 4 )
        
        time.sleep( 6 )
        self.check_for_row_in_list_table( '1: Buy peacock feathers' )
        self.check_for_row_in_list_table( '2: Peacock can fly in the sky' )
        
        self.fail( 'Finish the test' )
        
if __name__ == "__main__":
    unittest.main()
