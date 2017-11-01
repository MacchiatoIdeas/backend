from exercises.serializers import (
	AutomatedExerciseSerializer,
	AutomatedExerciseListSerializer
)
from users.serializers import *
from .models import *


class ContentListSerializer(serializers.ModelSerializer):
	text = serializers.ReadOnlyField(source='abstract')
	author = TeacherSerializer(read_only=True)

	class Meta:
		model = Content
		fields = ('id', 'unit', 'title', 'summary', 'text', 'author','moment')


class GuideListSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)

	class Meta:
		model = Guide
		fields = ('id', 'user', 'title', 'brief','moment')


class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'name', 'color', 'thumbnail')


class SubjectListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'name', 'color', 'thumbnail')


class UnitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level')


class UnitRetrieveSerializer(serializers.ModelSerializer):
	contents = ContentListSerializer(many=True, read_only=True)
	exercises = AutomatedExerciseListSerializer(many=True, read_only=True)
	subject = SubjectSerializer(read_only=True)

	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level', 'contents', 'exercises')


class UnitWithSubjectRetrieveSerializer(serializers.ModelSerializer):
	subject = SubjectSerializer(read_only=True)

	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level')

# TODO: Considerate to destroy UnitListSerializer and replace it with UnitSerializer wherever it appears.
class UnitListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level')


class SubjectRetrieveSerializer(serializers.ModelSerializer):
	units = UnitListSerializer(many=True, read_only=True)
	guides = GuideListSerializer(source='guide_set', many=True, read_only=True)

	class Meta:
		model = Subject
		fields = ('id', 'name', 'units', 'color', 'thumbnail', 'guides')


class CommentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)

	# TODO: Should the content be retrieved?
	# content = ContentSerializer()

	class Meta:
		model = Comment
		fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)
	comments = CommentSerializer(many=True, read_only=True)

	class Meta:
		model = Content
		fields = ('id', 'unit','title', 'summary', 'text', 'author', 'comments','moment')


class ContentRetrieveSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)
	unit = UnitWithSubjectRetrieveSerializer()
	comments = CommentSerializer(many=True, read_only=True)

	class Meta:
		model = Content
		fields = ('id', 'unit', 'title', 'summary', 'text', 'author', 'comments','moment')


class FeedbackCommentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)

	class Meta:
		model = FeedbackComment
		fields = '__all__'


class ContentGuideSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)

	class Meta:
		model = Content
		fields = ('id', 'unit', 'title', 'summary', 'text', 'author', 'moment')


class GuideItemSerializer(serializers.ModelSerializer):
	type = serializers.SerializerMethodField()
	item = serializers.SerializerMethodField()

	class Meta:
		model = GuideItem
		fields = ('id','type','item','order')

	def get_type(self, gitem):
		if gitem.content is not None:
			return 'content'
		elif gitem.exercise is not None:
			return 'exercise'
		else:
			return 'unknown'

	def get_item(self, gitem):
		if gitem.content is not None:
			return ContentGuideSerializer(instance=gitem.content).data
		elif gitem.exercise is not None:
			return AutomatedExerciseSerializer(instance=gitem.exercise).data
		else:
			return None

class GuideItemInputSerializer(serializers.ModelSerializer):

	def validate(self, data):
		both = data['exercise'] and data['content']
		neither = not data['exercise'] and not data['content']
		if both or neither:
			raise serializers.ValidationError('Either exercise or content must be set')
		return data

	class Meta:
		model = GuideItem
		fields = ('id','guide','content','exercise','order')

class GuideSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	items = GuideItemSerializer(many=True, read_only=True)
	subject = SubjectSerializer(read_only=True)

	class Meta:
		model = Guide
		fields = ('id', 'user', 'title', 'brief', 'subject', 'items', 'private', 'moment')

class GuideInputSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)

	class Meta:
		model = Guide
		fields = ('id', 'user', 'title', 'brief', 'subject', 'private')
