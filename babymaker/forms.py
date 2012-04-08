from django import forms

from babymaker.models import Bookmark

import urllib2

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('url',)
        
    def __init__(self, *args, **kwargs):
        super(BookmarkForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['placeholder'] = "http://"
        self.fields['url'].widget.attrs['size'] = 100
        self.fields['url'].label = u"Paste URL of page here:"
        
    def clean_url(self):
        url = self.cleaned_data['url']
        print dir(url)
        print url
        try:
            content = urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            raise forms.ValidationError("Could not load the page at the URL specified.")
        return url
        