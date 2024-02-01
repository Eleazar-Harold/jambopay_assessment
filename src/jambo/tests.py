from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model as User
from jambo.models import Business, BusinessCategory, BusinessItem, Item

# Create your tests here.
# Testing user_business_create
class UserBusinessCreateTest(TestCase):
    # ----------------------------------------------------------------
    # Successful CSV import with new user creation
    # ----------------------------------------------------------------
    def test_successful_import_with_new_user(self):
        csv_data = b"""Customer name,Customer Phone number,Business Category,Business Name,Item,Amount,Year
                       John Doe,1234567890,Electronics,ABC Electronics,Laptop,50000,2023
                       """
        response = self.client.post(reverse('jambo:create'), {'csv_file': csv_data})
        self.assertRedirects(response, reverse('jambo:list'))


        # Assert user, category, business, item, and business item are created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BusinessCategory.objects.count(), 1)
        self.assertEqual(Business.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(BusinessItem.objects.count(), 1)

    # ----------------------------------------------------------------
    # CSV import with existing user
    # ----------------------------------------------------------------
    def test_import_with_existing_user(self):
        # Create an existing user
        User.objects.create_user(email='existing@example.com', full_name='John Doe')

        csv_data = b"""Customer name,Customer Phone number,Business Category,Business Name,Item,Amount,Year
                       John Doe,9876543210,Electronics,XYZ Electronics,Phone,30000,2023
                       """
        response = self.client.post(reverse('jambo:create'), {'csv_file': csv_data})
        self.assertRedirects(response, reverse('jambo:list'))

        # Assert only business, item, and business item are created (user already exists)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BusinessCategory.objects.count(), 1)
        self.assertEqual(Business.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(BusinessItem.objects.count(), 1)

    # ----------------------------------------------------------------
    # Invalid CSV file
    # ----------------------------------------------------------------
    def test_invalid_csv_file(self):
        csv_data = b"Invalid CSV data"
        response = self.client.post(reverse('jambo:create'), {'csv_file': csv_data})
        self.assertEqual(response.status_code, 200)  # Expecting a form error, not a redirect
        self.assertTrue(response.context['form'].errors)


# Testing user_business_list_view view
class UserBusinessListViewTest(TestCase):
    # ----------------------------------------------------------------
    # Pagination
    # ----------------------------------------------------------------
    def test_pagination(self):
        # Create 21 business items
        for i in range(21):
            BusinessItem.objects.create(user=User.objects.create_user(email=f'user{i}@example.com'),
                                        business=Business.objects.create(name=f'Business {i}'),
                                        item=Item.objects.create(name=f'Item {i}'))

        response = self.client.get(reverse('jambo:list'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items_page']), 10)  # Second page should have 10 items

    # ----------------------------------------------------------------
    # Invalid page number
    # ----------------------------------------------------------------
    def test_invalid_page_number(self):
        response = self.client.get(reverse('jambo:list'), {'page': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['items_page'].number, 1)  # Should default to first page
