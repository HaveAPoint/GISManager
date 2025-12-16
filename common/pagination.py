"""
通用分页器
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    标准分页器
    
    每页默认显示 20 条记录，最大每页 100 条
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

