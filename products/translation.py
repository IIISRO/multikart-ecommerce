from modeltranslation.translator import translator, TranslationOptions
from .models import Category

class CategoryTranslationOption(TranslationOptions):
    fields=('name',)

translator.register(Category, CategoryTranslationOption)    