from django.template.loader import render_to_string

def render_kclusters(kcluster, bookmarks, template_name="babymaker/cluster_list.html"):
    cluster_list = []
    for cluster in kcluster:
        cluster_number = kcluster.index(cluster)+1
        cluster_bookmarks = []
        for bookmark_index in cluster:
            bookmark = bookmarks[bookmark_index]
            cluster_bookmarks.append(bookmark)
        rendered_cluster = render_single_cluster(cluster_bookmarks, cluster_number)
        cluster_list.append(rendered_cluster)
    return render_to_string(template_name, locals())
    
def render_single_cluster(bookmarks, cluster_number, template_name="babymaker/single_cluster.html"):
    return render_to_string(template_name, locals())