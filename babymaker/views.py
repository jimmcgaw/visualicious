from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers, urlresolvers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from babymaker.models import Bookmark, WordCount
from babymaker.forms import BookmarkForm
from babymaker.blocks import render_kclusters

from BeautifulSoup import BeautifulSoup

import urllib2
import urllib
import nltk
import string
import datetime
import os
import re
import simplejson
import clusters

@login_required
def links(request, template_name="babymaker/links.html"):
    user = request.user
    bookmarks = user.bookmark_set.all()
    words = []
    title = u""
    form = BookmarkForm()
    
    if request.method == 'POST':
        url = request.POST.get('url', '')
        if url:
            bookmarks_found = Bookmark.objects.filter(url=url)
            if not bookmarks_found:
                title, word_counts = get_page_title_and_word_counts(url)
                if title and word_counts:
                    data = {
                        'url': url
                    }
                    form = BookmarkForm(data)
                    if form.is_valid():
                        bookmark = form.save(commit=False)
                        bookmark.user = user
                        bookmark.title = title
                        bookmark.save()
                        
                        url = u""

                        for word, count in word_counts.iteritems():
                            try:
                                wc = WordCount.objects.get(bookmark=bookmark, word=word)
                                wc.count = count
                            except WordCount.DoesNotExist:
                                wc = WordCount(bookmark=bookmark, word=word, count=count)
                            wc.save()
            
    return render(request, template_name, locals())
    
@login_required
def view_clusters(request, template_name="babymaker/clusters.html"):
    user = request.user
    kclusters = []
    k_value = 0
    cluster_list = None
    
    if request.GET.get('k', None):
        k_value = int(request.GET.get('k'))
        bookmarks, word_vectors = Bookmark.get_word_vectors_for_user(user)
        kclusters = clusters.kcluster(word_vectors, k=k_value)
        cluster_list = render_kclusters(kclusters, bookmarks)
    return render(request, template_name, locals())


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def get_page_title_and_word_counts(url):
    word_counts = {}
    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        title = soup('title')[0].getText()
        all_words = soup.findAll(text=True)
        words = filter(visible, all_words)
        words = [word.lower() for word in words if word != u"\n"]
        word_string = " ".join(words)
        tokens = nltk.tokenize.word_tokenize(word_string)
        for char in string.punctuation:
            while char in tokens:
                tokens.remove(char)
                
        for token in tokens:
            try:
                word_counts[token] += 1
            except:
                word_counts.setdefault(token, 1)
    except:
        pass
        
    return title, word_counts