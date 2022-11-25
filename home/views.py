from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
import datetime

# Create your views here.
class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()

class HomeView(BaseView):
    def get(self, request):
        self.views['categories'] = Category.objects.all()
        self.views['reviews'] = Review.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['news'] = Product.objects.filter(labels = 'new')
        self.views['hots'] = Product.objects.filter(labels = 'hot')
        self.views['sales'] = Product.objects.filter(labels = 'sale')

        return render(request,'index.html',self.views)
      
class CategoryView(BaseView):
    def get(self, request, slug):
        self.views
        ids = Category.objects.get(slug=slug).id
        self.views['catproducts']=Product.objects.filter(category_id = ids)
        return render(request,'category.html',self.views)
  

class ProductDetailView(BaseView):
    def get(self,request,slug):
        self.views['productdetails']=Product.objects.filter(slug=slug)
        subcat_ids =Product.objects.get(slug=slug).subcategory_id
        self.views['related_products']=Product.objects.filter(subcategory_id = subcat_ids)
        self.views['product_reviews']=ProductReview.objects.filter(slug=slug)
        return render(request,'product-detail.html',self.views)
        
class SearchProduct(BaseView):
    def get(self,request):
        self.views
        if request.method == 'GET':
            query = request.GET['query']
            if query == '':
                return redirect('/')
            else:
                self.views['search_pproduct'] = Product.objects.filter(title__icontains = query)
        return render(request, 'search.html', self.views)


def product_review(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        slug = request.POST['slug']
        review = request.POST['review']
        star = request.POST['star']
        x = datetime.datetime.now()
        date = x.strftime("%c")

        data = ProductReview.objects.create(
            name = name,
            email = email,
            slug = slug,
            review = review,
            star = star,
            date = date
        )
        data.save()
        return redirect(f'/product_detail/{slug}')



