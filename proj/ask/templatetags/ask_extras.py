from django import template

register = template.Library()

@register.inclusion_tag('ask/templatetags/pagination.html')
def pagination(paginator, current_page, url):
    num_pages = paginator.num_pages
    page_middle_start = current_page - 4
    page_middle_start = page_middle_start if page_middle_start > 0 else 1

    page_middle_end   = current_page + 4
    page_middle_end   = page_middle_end if page_middle_end <= num_pages else num_pages

    pages = list(range(page_middle_start, page_middle_end + 1))
    return {
        "pages":pages,
        "curr_page": current_page,
        "url": url,
        "num_pages": num_pages,
        "page_middle_start": page_middle_start,
        "page_middle_end": page_middle_end
    }