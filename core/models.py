from django.db import models
from django.conf import settings
from django.db.models.aggregates import Sum


class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')
        return qs

    def all_with_related_persons_and_score(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum('vote__vote'))
        return qs


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(
                movie=movie,
                user=user
            )
        except Vote.DoesNotExist:
            return Vote(movie=movie,
                        user=user)


class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.died:
            return '{} {} ({} - {})'.format(
                self.first_name,
                self.last_name,
                self.born.born,
                self.died.died
            )
        else:
            return '{} {} ({})'.format(
                self.first_name,
                self.last_name,
                self.born.born
            )

    @property
    def full_name(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audience'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted'),
    )
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS,
                                 default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField()
    director = models.ForeignKey(to=Person,
                                 related_name='directed',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    writers = models.ManyToManyField(to=Person,
                                     related_name='writing_credits',
                                     blank=True)
    actors = models.ManyToManyField(to=Person,
                                    through='Role',
                                    related_name='acting_credits',
                                    blank=True)
    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')

    def __str__(self):
        return '{} {}'.format(self.title, self.year)


class Role(models.Model):
    movie = models.ForeignKey(to=Movie,
                              on_delete=models.DO_NOTHING)
    person = models.ForeignKey(to=Person,
                               on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return "{} {} {}".format(self.movie_id,
                                 self.person_id,
                                 self.name)

    class Meta:
        unique_together = ('movie',
                           'person',
                           'name')


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VOTE_CHOICES = (
        (UP, 'THUMBS UP'),
        (DOWN, 'THUMBS DOWN'),
    )
    movie = models.ForeignKey(to=Movie,
                              on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return '{} {} {}'.format(
            self.movie,
            self.person.full_name,
            self.choice
        )
