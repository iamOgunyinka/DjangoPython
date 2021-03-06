from django.test import TestCase
from lists.models import Item
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from lists.views import home_page

strn_r = 'A new list item'

class HomePageTest( TestCase ):
  def test_root_url_resolves_to_home_page_view( self ):
    found = resolve( '/' )
    self.assertEqual( found.func, home_page )

  def test_home_page_display_all_lists_items( self ):
    Item.objects.create( text='Itemey 1' )
    Item.objects.create( text='Itemey 2' )

    request = HttpRequest()
    response = home_page( request )

    self.assertIn( 'Itemey 1', response.content.decode() )
    self.assertIn( 'Itemey 2', response.content.decode() )

  def test_home_page_returns_correct_html( self ):
    request = HttpRequest()
    response = home_page( request )
    expected_html = render_to_string( 'home.html',
      { 'new_item_text', strn_r } )
    self.assertEqual( response.content.decode(), expected_html )

  def test_homepage_can_save_POST_request( self ):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = strn_r

    response = home_page( request )
    
    self.assertEqual( Item.objects.count(), 1 )
    new_item = Item.objects.first()
    self.assertEqual( strn_r, new_item.text )
    
    self.assertEqual( response.status_code, 302 ) #test for redirection
    self.assertIn( response['location'], '/' )

class ItemModelTest( TestCase ):
  def test_saving_and_retrieving_items( self ):
    first_str, second_str = 'The first(ever) item saved', 'Second item'
    first_item = Item()
    first_item.text = first_str
    first_item.save()
    
    second_item = Item()
    second_item.text = second_str
    second_item.save()
    
    saved_items = Item.objects.all()
    self.assertEqual( saved_items.count(), 2 )
    
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    
    self.assertEqual( first_saved_item.text, first_str )
    self.assertEqual( second_saved_item.text, second_str )
    
