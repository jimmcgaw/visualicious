from django.db import models

from BeautifulSoup import BeautifulSoup

import urllib2
import urllib
import nltk
import string


class Bookmark(models.Model):
    user = models.ForeignKey("auth.User")
    url = models.URLField()
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
         
    @classmethod
    def get_word_vectors_for_user(cls, user):
        word_vectors = []
        common_words = WordCount.get_common_words_for_user(user)
        user_bookmarks = cls.objects.filter(user=user)
        for bookmark in user_bookmarks:
            print "Checking bookmark #%d" % bookmark.id
            word_vector = bookmark.get_word_vector(common_words)
            word_vectors.append(word_vector)
        return user_bookmarks, word_vectors
         
    def get_word_vector(self, word_list):
        word_vector = []
        for word in word_list:
            print "Checking word %s" % word
            word_count = self.wordcount_set.filter(word=word).count()
            word_vector.append(word_count)
        print word_vector
        return word_vector
             
    
    
class WordCount(models.Model):
    bookmark = models.ForeignKey("babymaker.Bookmark")
    word = models.TextField()
    count = models.PositiveIntegerField(default=0)
    
    @classmethod
    def get_common_words_for_user(cls, user):
        common_words = []
        word_counts = cls.objects.filter(bookmark__user=user)
        total_word_count = sum([wc.count for wc in word_counts])
        
        words = list(set([wc.word for wc in word_counts]))
        for word in words:
            #print "Checking if %s is a common word" % word
            word_counts = cls.objects.filter(word=word)
            count_for_word = sum([wc.count for wc in word_counts])
            proportion = float(count_for_word)/float(total_word_count)
            proportion = proportion*1000
            if proportion > 0.3 and proportion < 0.5:
                common_words.append(word)
        print common_words
        return common_words
    



def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def get_page_words(url):
    words = []
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
        words = list(set(tokens))
    except:
        pass
        
    return title, word_counts