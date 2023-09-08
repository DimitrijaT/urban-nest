from django.contrib.auth.models import User

from Furniture.models import Category, FrontCover, UrbanNestUser, About, Contact, ShoppingCart, FurnitureAd


class CommonDatabaseSetup:
    def setUpDatabase(self):
        self.frontCover = FrontCover.objects.create(
            active=True,
            title='test_title',
            subtitle_1='test_subtitle_1',
            subtitle_2='test_subtitle_2',
            buy_button='test_buy_button_text',
            sell_button='test_sell_button_text',
            cover_page=None
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )

        self.urbanNestUser = UrbanNestUser.objects.create(
            user=self.user,
            first_name='test_first_name',
            last_name='test_last_name',
            phone_number='+38975218410',
            address='UL 1 BR. 105 A',
            city='Skopje',
            province='test_province',
            postal_code='1000',
            country='MK',
        )
        self.urbanNestUser2 = UrbanNestUser.objects.create(
            user=self.user2,
            first_name='test_first_name2',
            last_name='test_last_name2',
            phone_number='123456789',
            address='test_address2',
            city='test_city2',
            province='test_province2',
            postal_code='1000',
            country='RU',
        )

        self.shopping_cart = ShoppingCart.objects.create(
            buyer=self.urbanNestUser,
        )
        self.shopping_cart2 = ShoppingCart.objects.create(
            buyer=self.urbanNestUser2,
        )
        self.category = Category.objects.create(
            name='test_category',
            photo=None
        )
        self.urbanNestUser.shopping_cart = self.shopping_cart

        self.urbanNestUser2.shopping_cart = self.shopping_cart2

        self.shopping_cart.items.set([])
        self.shopping_cart2.items.set([])

        self.urbanNestUser.save()
        self.urbanNestUser2.save()
        self.shopping_cart2.save()
        self.shopping_cart.save()
        self.user.save()
        self.user2.save()

        self.about = About.objects.create(
            title='test_title',
            description='test_description',
            image=None
        )
        self.contact = Contact.objects.create(
            user=self.urbanNestUser,
            name='test_name',
            email='test_email',
            message='test_message'
        )

    def tearDownDatabase(self):
        self.frontCover.delete()
        self.user.delete()
        self.user2.delete()
        self.urbanNestUser.delete()
        self.urbanNestUser2.delete()
        self.shopping_cart.delete()
        self.shopping_cart2.delete()
        self.category.delete()
        self.about.delete()
        self.contact.delete()
