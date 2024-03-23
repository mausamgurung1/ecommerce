from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import permissions as pd
from . import serializers
from .filters import ProductFilter
from .models import Cart, Category, Product

# Create your views here.


class CategoryViewset(ModelViewSet):
   queryset=Category.objects.all()
   serializer_class = serializers.CateogrySerializer


    
class ProductViewset(ModelViewSet):
    queryset=Product.objects.select_related('category').all()
    serializer_class=serializers.ProductSerializer
    filter_backends =(DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_class  = ProductFilter
    search_fields =['name',]
    ordering_fields=['price']
    pagination_class=PageNumberPagination
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]


class CartViewset(generics.CreateAPIView,generics.ListAPIView):
   # serializer_class=serializers.CartSerializer
   # queryset=Cart.objects.prefetch_related('cart_items__product').all()
   permission_classes=[permissions.IsAuthenticated]
   
   
   def get_queryset(self):
       return Cart.objects\
          .prefetch_related('cart_items')\
          .filter(user=self.request.user)
          
   
   
   def get_serializer_class(self):
      if self.request.method=="POST":
         return serializers.CreateCartSerializer
      
      return serializers.CartSerializer
   
