from django.db import models


class FieldOfStudy(models.Model):
    """
    Field of Study as in Mathematics, History, etc.
    """

    # name of this field of study.
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    Unit of a particular field of study, for example Differential equations.
    """

    # area containing this unit.
    area = models.ForeignKey(FieldOfStudy, related_name='units',
                             on_delete=models.CASCADE)

    # name of this unit.
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SubUnit(models.Model):
    """
    Sub unit is pretty much just a deeper unit.
    """

    # unit is the higher level unit.
    unit = models.ForeignKey(Unit, related_name='sub_units',
                             on_delete=models.CASCADE)

    # name of this sub unit.
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    """
    A Subject Matter is a submission of a teacher to a certain Sub Unit.
    """

    # sub unit which will contain this subject matter.
    sub_unit = models.ForeignKey(SubUnit, related_name='contents',
                                 on_delete=models.CASCADE)

    # author owner of this content.
    author = models.ForeignKey("users.Teacher", on_delete=models.CASCADE)

    # text of this content.
    text = models.TextField()

    def __str__(self):
        return str(self.sub_unit)


class Comment(models.Model):
    """
    Comment on a content.
    """

    # user who wrote the comment.
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # content related.
    content = models.ForeignKey(Content, related_name='comments',
                                on_delete=models.CASCADE)

    # text of this comment.
    text = models.TextField()


class FeedbackComment(models.Model):
    """
    Feedback Comment on a content.
    """

    # user who wrote the comment.
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    # content related.
    content = models.ForeignKey(Content, related_name='feedback_comments',
                                on_delete=models.CASCADE)

    # quoted section to feedback on.
    quote = models.TextField()

    # text of this comment.
    text = models.TextField()
