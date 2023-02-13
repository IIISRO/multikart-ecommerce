#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multicart.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



# from products.models import *

# clothing=Category(name='Clothing', parent_id=None)
# clothing.save()

# bags=Category(name='Bags', parent_id=None)
# bags.save()

# footwear=Category(name='Footwear', parent_id=None)
# footwear.save()

# watchs=Category(name='Watches', parent_id=None)
# watchs.save()

# house=Category(name='House of Design', parent_id=None)
# house.save()

# beauty=Category(name='Beauty & Personal care', parent_id=None)
# beauty.save()

# home=Category(name='Home & Decor', parent_id=None)
# home.save()

# kitchen=Category(name='Kitchen', parent_id=None)
# kitchen.save()

# women=Category(name="Women's fashion", parent_id=clothing)
# women.save()

# men=Category(name="Men's fashion", parent_id=clothing)
# men.save()

# accessories=Category(name="Accessories", parent_id=clothing)
# accessories.save()

# dresses=Category(name="Dresses", parent_id=women)
# dresses.save()

# skirts=Category(name="Skirts", parent_id=women)
# skirts.save()

# westarn=Category(name="Westarn wear", parent_id=women)
# westarn.save()

# ethic=Category(name="Ethic wear", parent_id=women)
# ethic.save()

# sport=Category(name="Sport wear", parent_id=women)
# sport.save()

# mensport=Category(name="Sport wear", parent_id=men)
# mensport.save()

# menwestrn=Category(name="Westarn wear", parent_id=men)
# menwestrn.save()

# menethic=Category(name="Ethic wear", parent_id=men)
# menethic.save()

# fashion=Category(name="Fashion jewellery", parent_id=accessories)
# fashion.save()

# caps=Category(name="Caps and hats", parent_id=accessories)
# caps.save()

# precius=Category(name="Precious jawellery", parent_id=accessories)
# precius.save()

# necklaces=Category(name="Necklaces", parent_id=accessories)
# necklaces.save()

# earings=Category(name="Earings", parent_id=accessories)
# earings.save()

# wrist=Category(name="Wrist wear", parent_id=accessories)
# wrist.save()


# ties=Category(name="Ties", parent_id=accessories)
# ties.save()


# cufflinks=Category(name="Cufflinks", parent_id=accessories)
# cufflinks.save()


# pocket=Category(name="Pockets squares", parent_id=accessories)
# pocket.save()


# shopper=Category(name="Shopper bags", parent_id=bags)
# shopper.save()

# laptop=Category(name="Laptop bags", parent_id=bags)
# laptop.save()

# cluthec=Category(name="Clutches", parent_id=bags)
# cluthec.save()

# purses=Category(name="Purses", parent_id=bags)
# purses.save()

# subpurses=Category(name="Purses", parent_id=purses)
# subpurses.save()

# wallets=Category(name="Wallets", parent_id=purses)
# wallets.save()

# leathers=Category(name="Leathers", parent_id=purses)
# leathers.save()

# satchels=Category(name="Satchels", parent_id=purses)
# satchels.save()

# sportshoes=Category(name="Sport shoes", parent_id=footwear)
# sportshoes.save()

# formalshoes=Category(name="Formal shoes", parent_id=footwear)
# formalshoes.save()

# casualshoes=Category(name="Casual shoes", parent_id=footwear)
# casualshoes.save()

# makeup=Category(name="Makeup", parent_id=beauty)
# makeup.save()

# skincare=Category(name="Skincare", parent_id=beauty)
# skincare.save()


# premium=Category(name="Premium beauty", parent_id=beauty)
# premium.save()


# more=Category(name="More", parent_id=beauty)
# more.save()

# fragrances=Category(name="Fragrances", parent_id=more)
# fragrances.save()

# luxury=Category(name="Luxury beauty", parent_id=more)
# luxury.save()

# hair=Category(name="Hair care", parent_id=more)
# hair.save()

# tools=Category(name="Tools & brushes", parent_id=more)
# tools.save()




        
