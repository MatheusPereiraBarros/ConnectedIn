from django.core.files.images import get_image_dimensions
from django import forms


class FormPost(forms.Form):

    content = forms.CharField(max_length=256, required=True)
    image = forms.ImageField(required=False)

    def is_valid_from_form(self):
        return super(FormPost, self).is_valid()

    def verify_image(self, request):
        if 'image' in request.FILES and (request.FILES['image'] is not None or request.FILES['image'] is not ''):
            image = request.FILES['image']
            try:
                main, sub = image.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'jpg', 'png']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                                                'JPG or PNG image.')
            except AttributeError:
                pass
            return image
        else:
            return None