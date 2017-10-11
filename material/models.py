from django.db import models
from os.path import splitext
from exercises.models import AutomatedExercise
from users.models import Course

from primitivizer import primitivize_string


def generate_thumbnail_path(instance, filename):
    return 'images/field_thumbnail/{0}.{1}'.format(instance.name,
                                                   splitext(filename)[1])


class Subject(models.Model):
    """
    Field of Study as in Mathematics, History, etc.
    """

    # name of this field of study.
    name = models.CharField(max_length=50, unique=True)

    # color #xxxxxxx (7 chars max)
    color = models.CharField(max_length=7)

    # field's image
    #thumbnail = models.ImageField(upload_to=generate_thumbnail_path, null=True)
    thumbnail = models.URLField(default='', blank=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    Unit of a particular field of study, for example Differential equations.
    """

    # area containing this unit.
    subject = models.ForeignKey(Subject, related_name='units',
                                on_delete=models.CASCADE)

    # name of this unit.
    name = models.CharField(max_length=50, unique=True)

    # 1st grade, 2nd grade, ...
    academic_level = models.IntegerField()

    def __str__(self):
        return self.name


class Content(models.Model):
    """
    A Subject Matter is a submission of a teacher to a certain Unit.
    """

    # unit which will contain this subject matter.
    unit = models.ForeignKey(Unit, related_name='contents',
                             on_delete=models.CASCADE)

    # author owner of this content.
    author = models.ForeignKey("users.Teacher", related_name='contents', on_delete=models.CASCADE)

    # keep it atomic
    subtitle = models.CharField(max_length=150)

    # summary of content
    summary = models.CharField(max_length=150)

    # text of this content.
    text = models.TextField()

    # editable html text of this content.
    html_text = models.TextField()

    def __str__(self):
        return str(self.unit)

    def abstract(self):
        # FIXME: use a real approach.
        return self.text[0:170]

    def serialize(self):
        pass

    # Primitivized version for searching
    primitive = models.TextField(blank=True)

    def make_primitive(self):
        return primitivize_string(" ".join([
            str(self.author),self.subtitle,self.summary,self.text]))


class Comment(models.Model):
    """
    Comment on a content.
    """

    # user who wrote the comment.
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)

    # content related.
    content = models.ForeignKey(Content, related_name='comments',
                                on_delete=models.CASCADE)

    # text of this comment.
    text = models.TextField()

    def __str__(self):
        return self.text


class FeedbackComment(models.Model):
    """
    Feedback Comment on a content.
    """

    # user who wrote the comment.
    user = models.ForeignKey("auth.User", related_name='feedback_comments', on_delete=models.CASCADE)

    # content related.
    content = models.ForeignKey(Content, related_name='feedback_comments',
                                on_delete=models.CASCADE)

    # quoted section to feedback on.
    quote = models.TextField()

    # text of this comment.
    text = models.TextField()

    def __str__(self):
        return self.text


class Guide(models.Model):
    """
    Ordered collection of content and material
    """

    # user who wrote the Guide
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    # subject of the guide
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # guide title
    title = models.TextField(max_length=64)

    # brief text
    brief = models.TextField(max_length=140)

    def __str__(self):
        return self.title

    # If it belongs to a course or it is public:
    course = models.ForeignKey(Course, null=True, blank=True,
            on_delete=models.CASCADE)



class GuideItem(models.Model):
    """
    Generic guide item
    """

    # Belongs to Guide
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE,
        related_name='items')

    # Either content
    content = models.ForeignKey(Content, blank=True, null=True)

    # Or exercise
    exercise = models.ForeignKey(AutomatedExercise, blank=True, null=True)

    # Order in guide
    order = models.IntegerField()

    class Meta:
        unique_together = ('guide', 'order')
        ordering = ['order']

    def __str__(self):
        return "guide: {0}, order: {1}".format(self.guide.title, self.order)
