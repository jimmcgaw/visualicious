#!/usr/bin/python

import os
import sys

sys.path.append("/Users/smoochy/aptana/visualicious")

os.environ['DJANGO_SETTINGS_MODULE'] = 'visualicious.settings'

#import clusters
#blog_names, words, data = clusters.readfile('blogdata.txt')
#print clusters.kcluster(data, k=10)

from django.contrib.auth.models import User

from babymaker.models import Bookmark



user = User.objects.get(username="smoochy")
Bookmark.get_word_vectors_for_user(user)