from django import template

register = template.Library()


@register.filter(name='paginate_range')
def paginate_range(page_obj, backfront=2):
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages
    # Calculate start and end page numbers
    start_page = max(current_page - backfront, 1)
    end_page = min(current_page + backfront, total_pages)

    # Generate the range of page numbers
    return range(start_page, end_page + 1)
