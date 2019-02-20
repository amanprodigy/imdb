from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from .models import Movie
from .views import MovieList


class MovieListPaginationTestCase(TestCase):

    """Test case to test pagination of movie listing"""

    ACTIVE_PAGINATION_HTML = """
    <li class="page-item active">
        <a class="page-link" href="{}?page={}">{}</a>
    </li>
    """

    def setUp(self):
        """
        create a set of 15 movies
        """
        for n in range(15):
            Movie.objects.create(title='Movie {}'.format(n),
                                 year=1990+n,
                                 runtime=100)

    def testFirstPage(self):
        movie_list_path = reverse('core:movie-list')
        request = RequestFactory().get(path=movie_list_path)
        response = MovieList.as_view()(request)
        self.assertEqual(200, response.status_code)
        print(response.context_data)
        self.assertTrue(response.context_data['is_paginated'])
        self.assertInHTML(
            self.ACTIVE_PAGINATION_HTML.format(
                movie_list_path, 1, 1
            ),
            response.rendered_content
        )
