def is_ajax(request) -> bool:
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def paragraphize(lines: list[str]) -> str:
    # Add trailing space so that screen readers read correctly.
    paragraphs = [f"<p>{line}</p><br>" for line in lines]
    return "".join(paragraphs)
