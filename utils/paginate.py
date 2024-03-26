'''
custom pagination function
'''
def paginate(data, page):
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
    return items_on_page, total_pages, custom_range