from django.urls import reverse

from wagtail.tests.utils.form_data import (
    nested_form_data,
    rich_text,
    streamfield,
)

import pytest
from bs4 import BeautifulSoup
from pytest_django.asserts import assertContains


@pytest.mark.django_db
def test_insert_editor_css(admin_client, root_page):
    response = admin_client.get('/admin/pages/%d/edit/' % root_page.id)
    assertContains(response, 'wagtail_cblocks/css/editor.css')


@pytest.mark.django_db
class TestStylizedStructBlock:
    def test_page_preview(self, admin_client, root_page):
        add_url = reverse(
            'wagtailadmin_pages:add',
            args=('tests', 'standardpage', root_page.id),
        )

        form_data = nested_form_data(
            {
                'title': "A page",
                'body': streamfield(
                    [
                        (
                            'hero_block',
                            {
                                'style': 'centered',
                                'blocks': streamfield(
                                    [
                                        (
                                            'paragraph_block',
                                            rich_text('<p>Lorem ipsum</p>'),
                                        ),
                                    ]
                                ),
                            },
                        ),
                    ]
                ),
            }
        )
        response = admin_client.post(add_url, data=form_data)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, 'html5lib')
        preview_url = soup.select_one('.button.action-preview')['data-action']

        form_data['slug'] = 'a-page'
        response = admin_client.post(preview_url, data=form_data)
        assert response.status_code == 200
        assert response.json()['is_valid'] is True

        response = admin_client.get(preview_url)
        assert response.status_code == 200
        assertContains(response, 'hero-centered')
        assertContains(response, 'Lorem ipsum')
