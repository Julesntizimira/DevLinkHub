'''
custom pagination function
'''
import os


if os.getenv('DOMAIN_NAME'):
    domain = os.getenv('DOMAIN_NAME')
else:
    domain = 'http://127.0.0.1:5100'


def paginate(data, page=1):
    '''handle pagination
    '''
    per_page = 9
    # Based on page and per_page info, calculate start and end index of items to keep
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    total_pages = (len(data) + per_page - 1) // per_page
    # Get the paginated list of items
    items_on_page = data[start_index:end_index]
    # Create Pagination object
    leftindex = page - 4 if page > 4 else 1
    rightIndex =  page + 5 if (page + 5) <= total_pages else total_pages + 1
    custom_range = range(leftindex, rightIndex)
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page + 1 <= total_pages else None
    result = {
        'page': page,
        'page_size': len(items_on_page),
        'prev_page': prev_page,
        'next_page': next_page,
        'total_pages': total_pages,
        'custom_range': custom_range,
        'items_on_page': items_on_page,
    }
    return result

def apiPagination(data, request):
    '''paginate api result'''
    page = request.args.get('page')
    if page:
        page = int(request.args.get('page'))
    else:
        page = 1
    pagination = paginate(data, page)
    result = {
        'Page': pagination['page'],
        'Page size': pagination['page_size'],
        'Previous page': pagination['prev_page'],
        'Next page': pagination['next_page'],
        'Total pages': pagination['total_pages'],
        'Data': pagination['items_on_page'],
        'Go back to home': f'{domain}/api/v1'
    }
    return result