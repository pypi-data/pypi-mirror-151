from bs4 import BeautifulSoup


def parse_page(page_content: str):
    nil = {'*': ()}
    return BeautifulSoup(page_content, 'html5lib', multi_valued_attributes=nil)


def get_canonical_url(page_content: str):
    page = parse_page(page_content)
    link = page.find('link', {'rel': 'canonical'})
    if link is not None:
        canonical_url: str = link.get('href')  # type: ignore
        return canonical_url


def get_epicgames_picture_url(page_content: str, egsid: str):
    page = parse_page(page_content)
    try:
        section = page.find('section', {'data-component': 'BrowseGrid'})
        assert section is not None

        a = section.find(
            'a',
            {
                'role': 'link',
                'href': '/en-US/p/' + egsid,
            },  # type: ignore
        )
        assert a is not None

        picture = a.find('img', {'data-component': 'FallbackImage'})  # type: ignore
        assert picture is not None

        picture_url: str = picture.get('data-image')  # type: ignore
        assert picture_url
        return picture_url

    except AssertionError:
        pass
