"""
# starting commands
    - py -m pip install django
    - pip3 install djangorestframework
    - pip3 install djangorestframework-simplejwt
    - django-admin startproject Articles
    - cd Articles
    - py manage.py startapp ArticlesApp
    - py manage.py startapp Accounts
"""

'''
# Endpoints:
    # Accounts:
        http://127.0.0.1:8000/register/
        http://127.0.0.1:8000/login/
    
    # Book Marks:
        http://127.0.0.1:8000/add_bookmark/<article_id>/
        http://127.0.0.1:8000/all_bookmark/
        http://127.0.0.1:8000/delete_bookmark/<bookmark_id>/
    
    # Comments:
        http://127.0.0.1:8000/add_comment/
        http://127.0.0.1:8000/view_comment/<article_id>/
        http://127.0.0.1:8000/delete_comment/<comment_id>/
    
    # Articles:
        http://127.0.0.1:8000/add_article/
        http://127.0.0.1:8000/update_article/<article_id>/
        http://127.0.0.1:8000/delete_article/<article_id>/
        http://127.0.0.1:8000/all_articles/
        http://127.0.0.1:8000/posted_articles_per_publisher/
        http://127.0.0.1:8000/posted_articles_per_category/<category_id>/
        http://127.0.0.1:8000/top5/
        http://127.0.0.1:8000/search/
        http://127.0.0.1:8000/article_details/<article_id>/

        http://127.0.0.1:8000/add_ArticleLike/<article_id>/
    
    # Category: 
        http://127.0.0.1:8000/all_categories/
        
        
    # Favourite Category:
    
        http://127.0.0.1:8000/add_favCategory/<category_id>/
        http://127.0.0.1:8000/list_favCategory/
        http://127.0.0.1:8000/delete_favCategory/<bookmark_id>/
    
    

'''
