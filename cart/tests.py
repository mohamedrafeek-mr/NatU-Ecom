from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ecompro.products.models import Product, Category
from ecompro.coupons.models import Coupon
from ecompro.cart.models import CartItem


class CartTests(TestCase):
    def setUp(self):
        # create a category and a product used across tests
        self.cat = Category.objects.create(name='Test Cat', slug='test-cat')
        self.product = Product.objects.create(
            category=self.cat,
            name='Test Product',
            slug='test-product',
            price=100,
            stock=10,
        )

    def test_coupon_form_visible_and_apply(self):
        client = self.client
        # add product to cart so form appears
        resp = client.post(reverse('cart:add', args=[self.product.id]))
        self.assertRedirects(resp, reverse('cart:detail'))

        resp = client.get(reverse('cart:detail'))
        self.assertContains(resp, 'Coupon code')

        # create a valid coupon
        coupon = Coupon.objects.create(
            code='TEST10',
            discount_amount=10,
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            active=True,
        )
        resp = client.post(reverse('coupons:apply'), {'code': 'TEST10'})
        self.assertRedirects(resp, reverse('cart:detail'))
        # session should hold coupon_id
        self.assertEqual(client.session.get('coupon_id'), coupon.id)

    def test_buy_now_adds_and_redirects(self):
        client = self.client
        # login a user to avoid login redirect
        user = self._create_user()
        client.force_login(user)

        resp = client.post(reverse('cart:buy', args=[self.product.id]))
        # should redirect to order creation (login may then redirect again)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('orders:create'))
        # fetch cart directly for user
        from ecompro.cart.models import Cart
        cart = Cart.objects.get(user=user)
        self.assertEqual(cart.items.count(), 1)
        item = cart.items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 1)

    def _create_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(username='testuser', password='pass')

