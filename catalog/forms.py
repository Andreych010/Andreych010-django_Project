from django import forms
from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)

    def clean_name(self):
        '''
        исключает загрузку запрещенных товаров
        '''
        clean_data = self.cleaned_data['name'].lower()
        not_valid = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for i in not_valid:
            if clean_data == i:
                raise forms.ValidationError('В наименование товара не могут использоваться следующие значения:'
                                            '\nказино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар.')
        return clean_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class ModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('preview', 'user', 'name', 'purchase_price',)
