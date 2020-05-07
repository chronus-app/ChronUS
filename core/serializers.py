from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from rest_framework import serializers
from core.models import Student, Degree, Competence, CollaborationRequest, Collaboration
from core.exceptions import ResourcePermissionException
from chat.models import Message
from drf_extra_fields.fields import Base64ImageField
from datetime import date


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5, 'max_length': 32}}
    
    def create(self, validated_data):

        return get_user_model().objects.create_user(**validated_data)


class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ('name', 'higher_grade', 'finished',)
    
    def validate(self, data):

        if data['finished'] == False and data['higher_grade'] == '':
            raise serializers.ValidationError('If the degree is not finished, the higher grade must not be blank')

        if data['finished'] == True and data['higher_grade'] is not '':
            raise serializers.ValidationError('You cannot specify a higher grade if the degree is finished')

        return data


class CompetenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competence
        fields = ('name',)


class StudentSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)
    profile_image = Base64ImageField(required=False)
    degrees = DegreeSerializer(many=True, required=True, allow_empty=False)
    competences = CompetenceSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = ('description', 'user', 'profile_image', 'degrees', 'competences',)

    @atomic
    def create(self, validated_data):

        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student = Student.objects.create(
                            user=user,
                            description=validated_data.pop('description', ''),
                            profile_image=validated_data.pop('profile_image', '')
                            )

        degrees_data = validated_data.pop('degrees')
        if degrees_data:
            for degree in degrees_data:
                Degree.objects.create(
                    name=degree['name'],
                    higher_grade=degree['higher_grade'],
                    finished=degree['finished'],
                    student=student
                )
        
        competences_data = validated_data.pop('competences', None)
        if competences_data:
            for competence in competences_data:
                retrieved_competence = get_object_or_404(Competence, name=competence['name'])
                retrieved_competence.students.add(student)
                student.competences.add(retrieved_competence)

        return student


class StudentShortSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Student
        fields = ('id', 'full_name', 'profile_image', 'average_rating',)
        read_only_fields = ('id',)


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                msg = 'Unable to authenticate with provided credentials'
                raise serializers.ValidationError(msg, code='authentication')
            
            data['user'] = user
            return data


class CollaborationRequestSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    competences = CompetenceSerializer(many=True, required=False)
    applicant = StudentShortSerializer(read_only=True)
    offerers = StudentShortSerializer(many=True, read_only=True)

    class Meta:
        model = CollaborationRequest
        fields = ('id','title', 'description', 'requested_time', 'deadline', 'competences', 'applicant', 'offerers')
        read_only_fields = ('id', 'applicant', 'offerers')
    
    def validate(self, data):

        applicant = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            applicant = request.user.student

        if data['requested_time'] > applicant.available_time:
            raise serializers.ValidationError('The requested time must be less than or equal to your available time')

        if data['deadline'] < date.today():
            raise serializers.ValidationError('The deadline must be greater than or equal to the current date')
        
        return data
    
    @atomic
    def create(self, validated_data):

        applicant = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            applicant = request.user.student
        
        applicant.available_time -= validated_data['requested_time']
        applicant.save()

        collaboration_request = CollaborationRequest.objects.create(
                        title=validated_data.pop('title'),
                        description=validated_data.pop('description', ''),
                        requested_time=validated_data.pop('requested_time'),
                        deadline=validated_data.pop('deadline'),
                        applicant=applicant
                        )
        
        competences_data = validated_data.pop('competences', None)
        if competences_data:
            for competence in competences_data:
                retrieved_competence = get_object_or_404(Competence, name=competence['name'])
                retrieved_competence.collaboration_requests.add(collaboration_request)

        return collaboration_request


class CollaborationRequestOfferSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    offerers = StudentShortSerializer(many=True, read_only=True)

    class Meta:
        model = CollaborationRequest
        fields = ('id', 'offerers',)
    
    def update(self, instance, validated_data):

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            student = request.user.student

        if student == instance.applicant:
            raise ResourcePermissionException('You cannot offer collaboration in one of your collaboration requests')

        if student in instance.offerers.all():
            raise ResourcePermissionException('You\'ve already offered to collaborate on this collaboration request')

        instance.offerers.add(student)
        return instance


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'text', 'read', 'timestamp', 'sender')


class CollaborationListSerializer(serializers.ModelSerializer):

    competences = CompetenceSerializer(many=True, required=False)

    class Meta:
        model = Collaboration
        fields = ('id', 'title', 'description', 'requested_time', 'deadline', 'competences',)


class CollaborationRetrieveSerializer(serializers.ModelSerializer):

    competences = CompetenceSerializer(many=True)
    applicant = StudentShortSerializer()
    collaborator = StudentShortSerializer()
    messages = MessageSerializer(many=True)

    class Meta:
        model = Collaboration
        fields = ('id', 'title', 'description', 'requested_time', 'deadline',
                 'competences', 'applicant', 'collaborator', 'messages',)
        

class CollaborationCreateSerializer(serializers.ModelSerializer):

    collaborator = serializers.IntegerField()
    collaboration_request = serializers.IntegerField()

    class Meta:
        model = Collaboration
        fields = ('collaborator', 'collaboration_request')
    
    @atomic
    def create(self, validated_data):

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            student = request.user.student
        
        collaboration_request = get_object_or_404(CollaborationRequest, id=validated_data['collaboration_request'])
        if collaboration_request.applicant != student:
            raise ResourcePermissionException('The collaboration request is not yours')

        collaborator = get_object_or_404(Student, user=validated_data['collaborator'])
        if collaborator not in collaboration_request.offerers.all():
            raise ResourcePermissionException('This student is not one of the collaboration request\'s colaborators')

        collaboration_request_data = {}
        collaboration_request_data['title'] = collaboration_request.title
        collaboration_request_data['description'] = collaboration_request.description
        collaboration_request_data['requested_time'] = collaboration_request.requested_time
        collaboration_request_data['deadline'] = collaboration_request.deadline

        collaboration = Collaboration.objects.create(**collaboration_request_data, applicant=student, collaborator=collaborator)
        
        for competence in collaboration_request.competences.all():
            collaboration.competences.add(competence)
        
        collaboration_request.delete()

        return collaboration
    
    def to_representation(self, instance):

        competences = instance.competences.all()
        competences_array = []
        for competence in competences:
            competence_obj = {}
            competence_obj['name'] = competence.name
            competences_array.append(competence_obj)

        collaborator = instance.collaborator
        collaborator_obj = {}
        collaborator_obj['id'] = collaborator.user.id
        collaborator_obj['full_name'] = collaborator.full_name
        collaborator_obj['profile_image'] = collaborator.profile_image if collaborator.profile_image else None
        collaborator_obj['average_rating'] = collaborator.average_rating

        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'requested_time': instance.requested_time,
            'deadline': instance.deadline,
            'competences': competences_array,
            'collaborator': collaborator_obj,
            'messages': []    
        }
        