import math

DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100


def clamp_per_page(per_page):
    if per_page is None:
        return DEFAULT_PER_PAGE
    return max(1, min(int(per_page), MAX_PER_PAGE))


def page_count(total, per_page):
    return max(1, math.ceil(total / per_page))


def paginate(items, page, per_page):
    # pages are 1-based: page 1 is the first page
    per_page = clamp_per_page(per_page)
    start = (page - 1) * per_page
    return items[start:start + per_page]


def page_links(base_url, page, total, per_page):
    last = page_count(total, per_page)
    links = {"self": base_url + "?page=" + str(page)}
    if page > 1:
        links["prev"] = base_url + "?page=" + str(page - 1)
    if page < last:
        links["next"] = base_url + "?page=" + str(page + 1)
    links["last"] = base_url + "?page=" + str(last)
    return links


def parse_page(raw):
    try:
        page = int(raw)
    except (TypeError, ValueError):
        return 1
    return page if page >= 1 else 1


def sort_items(items, key, descending):
    return sorted(items, key=lambda item: item[key], reverse=descending)


def filter_items(items, field, value):
    if value is None:
        return items
    return [item for item in items if item.get(field) == value]


def listing(items, raw_page, raw_per_page, base_url, sort_key="id", descending=False, status=None):
    items = filter_items(items, "status", status)
    items = sort_items(items, sort_key, descending)
    page = parse_page(raw_page)
    per_page = clamp_per_page(raw_per_page)
    return {
        "items": paginate(items, page, per_page),
        "page": page,
        "per_page": per_page,
        "total": len(items),
        "links": page_links(base_url, page, len(items), per_page),
    }
