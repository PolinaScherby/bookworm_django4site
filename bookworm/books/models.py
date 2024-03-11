from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager


User = get_user_model()


class PublishedManager(models.Manager):
    """A status for books newly added to the site."""
    def get_queryset(self):
        return super().get_queryset().filter(status=Book.Status.PUBLISHED)


class Book(models.Model):
    """
    Model representing a book.

    Attributes:
        title (CharField): The title of the book.
        author (ForeignKey): The author of the book.
        genre (ManyToManyField): The genre(s) of the book.
        first_published (IntegerField, optional): The year the book was first published.
        description (TextField, optional): A brief description of the book.
        quote (TextField, optional): A notable quote from the book.
        image (ImageField, optional): Image representing the book cover.
        slug (SlugField): The slugified version of the book's title for URL.
        time_create (DateTimeField): The date and time the book record was created.
        time_update (DateTimeField): The date and time the book record was last updated.
        tags (TaggableManager): Tags associated with the book.
        user (ForeignKey): The user who added the book.
        status (CharField): Indicates whether the book is published or in draft.

    Methods:
        average_rating(): Calculate the average rating of the book.
        get_absolute_url(): Get the canonical URL for the book detail page.

    """
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    genre = models.ManyToManyField('Genre', blank=True, related_name='books')
    first_published = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    quote = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default=None, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    tags = TaggableManager(ordering=["name"], blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None, related_name='books')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Save method to generate the slug."""
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def average_rating(self):
        """
        Calculate the average rating of the book.

        Returns:
            int: The average rating of the book.
        """
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            return round(total_rating / len(reviews))
        return 0

    def get_absolute_url(self):
        """
        Get the canonical URL for the book detail page.

        Returns:
            str: The URL of the book detail page.
        """
        return reverse('book', kwargs={'book_slug': self.slug})


class Author(models.Model):
    """
    Represents an author of a book.

    Attributes:
        name (CharField): The name of the author.
        description (TextField): A brief description or biography of the author.
        slug (SlugField): A slugified version of the author's name for use in URLs.
        photo (ImageField): An optional photo/image of the author.
    """
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    photo = models.ImageField(upload_to='photos/', default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the canonical URL for the author.

        Returns:
            str: The canonical URL for the author.
        """
        return reverse('author', kwargs={'author_slug': self.slug})


class Genre(models.Model):
    """
    Represents a genre/category of books.

    Attributes:
        title (CharField): The title of the genre.
        slug (SlugField): A slugified version of the genre's title for use in URLs.
    """
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        """
        Returns the canonical URL for the genre.

        Returns:
            str: The canonical URL for the genre.
        """
        return reverse('genre', kwargs={'genre_slug': self.slug})


class Review(models.Model):
    """
    Represents a review of a book written by a user.

    Attributes:
        book (ForeignKey): The book being reviewed.
        user (ForeignKey): The user who wrote the review.
        text (TextField): The text content of the review.
        time_create (DateTimeField): The date and time when the review was created.
        rating (IntegerField): The rating given by the user to the book (1 to 5).
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.text[:15]

    def save(self, *args, **kwargs):
        """
        Saves the review object.

        Checks if a review already exists for the same book by the same user.
        If not, saves the review object.
        """
        existing_review = Review.objects.filter(book=self.book, user=self.user).exists()
        if not existing_review:
            super().save(*args, **kwargs)
