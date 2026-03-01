from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from .models import Category, Product, ProductImage
from ecompro.coupons.models import Coupon


class ProductTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='TestCat', slug='test-cat')
        self.product = Product.objects.create(
            category=self.cat,
            name='Sample',
            slug='sample',
            price=50,
            stock=5,
        )

    def test_product_detail_shows_image_url(self):
        # attach a fake image to product
        img = SimpleUploadedFile('test.jpg', b'filedata', content_type='image/jpeg')
        ProductImage.objects.create(product=self.product, image=img)
        resp = self.client.get(reverse('products:detail', args=[self.product.slug]))
        # the response should contain the URL of the uploaded file
        expected_url = self.product.images.first().image.url
        self.assertContains(resp, expected_url)

    def test_admin_can_add_product(self):
        # set up an admin user and login
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        self.client.force_login(admin)

        add_url = reverse('admin:products_product_add')
        data = {
            'category': self.cat.pk,
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'desc',
            'price': '123.45',
            'stock': '10',
            'featured': 'on',
            'status': 'active',
            # inline management form fields for zero images
            'images-TOTAL_FORMS': '0',
            'images-INITIAL_FORMS': '0',
            'images-MIN_NUM_FORMS': '0',
            'images-MAX_NUM_FORMS': '1000',
        }
        resp = self.client.post(add_url, data, follow=True)
        # successful add redirects back to changelist
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'was added successfully')
        self.assertTrue(Product.objects.filter(slug='new-product').exists())

    def test_status_filters(self):
        # create draft product and ensure not on list or detail
        draft = Product.objects.create(
            category=self.cat,
            name='Draft',
            slug='draft',
            price=10,
            stock=5,
            status='draft',
        )
        resp = self.client.get(reverse('products:detail', args=[self.product.slug]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('products:detail', args=[draft.slug]))
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get(reverse('products:list'))
        self.assertNotContains(resp, 'Draft')

    def test_coupon_on_detail(self):
        # product detail should show coupon form
        resp = self.client.get(reverse('products:detail', args=[self.product.slug]))
        self.assertContains(resp, 'Coupon code')
        # apply coupon and ensure session set
        coupon = Coupon.objects.create(
            code='PAGE',
            discount_amount=5,
            valid_from=timezone.now()-timezone.timedelta(days=1),
            valid_to=timezone.now()+timezone.timedelta(days=1),
            active=True,
        )
        resp = self.client.post(reverse('coupons:apply'), {'code': 'PAGE'})
        self.assertRedirects(resp, reverse('cart:detail'))
        self.assertEqual(self.client.session.get('coupon_id'), coupon.id)

    def test_search_filters_list_view(self):
        # create another product so we can search specifically
        other = Product.objects.create(
            category=self.cat,
            name='AnotherItem',
            slug='another',
            price=20,
            stock=3,
        )
        resp = self.client.get(reverse('products:list'), {'q': 'Sample'})
        self.assertContains(resp, 'Sample')
        self.assertNotContains(resp, 'AnotherItem')
        # search case insensitive and substring
        resp = self.client.get(reverse('products:list'), {'q': 'ample'})
        self.assertContains(resp, 'Sample')

    def test_autocomplete_endpoint(self):
        # query should return json containing matching names
        Product.objects.create(
            category=self.cat,
            name='Alpha',
            slug='alpha',
            price=30,
            stock=1,
        )
        Product.objects.create(
            category=self.cat,
            name='Beta',
            slug='beta',
            price=30,
            stock=1,
        )
        url = reverse('products:autocomplete')
        resp = self.client.get(url, {'q': 'a'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # should include both names that contain 'a' (case insensitive)
        self.assertIn('Alpha', data.get('suggestions', []))
        self.assertIn('Beta', data.get('suggestions', []))
        # minimal length threshold isn't enforced server-side, just returns contains

    def test_category_context_processor(self):
        # make a hierarchy of categories
        parent = Category.objects.create(name='Parent', slug='parent')
        child = Category.objects.create(name='Child', slug='child', parent=parent)
        # fetch a page that uses base template, e.g. product_list
        resp = self.client.get(reverse('products:list'))
        self.assertEqual(resp.status_code, 200)
        # context processor should have added 'all_categories'
        cats = resp.context.get('all_categories')
        self.assertIsNotNone(cats)
        self.assertIn(parent, cats)
        # children accessible
        self.assertTrue(parent.children.filter(pk=child.pk).exists())
        # the rendered HTML for the dropdown should mark parent as selected when on its page
        resp2 = self.client.get(parent.get_absolute_url())
        self.assertContains(resp2, 'bg-gray-300')
        # category object coming from context should carry selected flag
        cats_resp = resp2.context.get('all_categories')
        self.assertIsNotNone(cats_resp)
        # find our parent within the queryset
        selected_cat = [c for c in cats_resp if c.slug == parent.slug][0]
        self.assertTrue(getattr(selected_cat, 'selected', False))
    
