from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from rest_framework import serializers
from core.models import Student, Degree, Competence, CollaborationRequest
from drf_extra_fields.fields import Base64ImageField
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5, 'max_length': 32}}
    
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class DegreeSerializer(serializers.ModelSerializer):
    """Degree serializer"""
    class Meta:
        model = Degree
        fields = ('name', 'higher_grade', 'finished',)
    
    def validate(self, data):
        """Check that if a degree is not finished, the higher grade must not be blank 
        and if a degree is finished, the higher grade must be blank"""
        if data['finished'] == False and data['higher_grade'] == '':
            raise serializers.ValidationError('If the degree is not finished, the higher grade must not be blank')

        if data['finished'] == True and data['higher_grade'] is not '':
            raise serializers.ValidationError('You cannot specify a higher grade if the degree is finished')

        return data


class CompetenceSerializer(serializers.ModelSerializer):
    """Competence serializer"""
    class Meta:
        model = Competence
        fields = ('name',)


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer"""
    user = UserSerializer(required=True)
    profile_image = Base64ImageField(required=False)
    degrees = DegreeSerializer(many=True, required=True, allow_empty=False)
    competences = CompetenceSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = ('description', 'user', 'profile_image', 'degrees', 'competences',)

    @atomic
    def create(self, validated_data):
        """Create a new student and return it"""
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
    """Short serializer for student"""
    id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Student
        fields = ('id', 'full_name', 'profile_image', 'average_rating',)
        read_only_field = ('id',)


class AuthTokenSerializer(serializers.Serializer):
    """Authentication token serializer"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        """Validate and authenticate the user"""
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
    """Collaboration request serializer"""
    id = serializers.IntegerField(read_only=True)
    competences = CompetenceSerializer(many=True, required=False)
    applicant = StudentShortSerializer(read_only=True)
    offerers = StudentShortSerializer(many=True, read_only=True)

    class Meta:
        model = CollaborationRequest
        fields = ('id','title', 'description', 'requested_time', 'deadline', 'competences', 'applicant', 'offerers')
        read_only_fields = ('id', 'applicant', 'offerers')
    
    def validate(self, data):
        """Check that the requested time is less than or equal to the applicant's available time.
           Check that the deadline is greater than or equal to the current date.
        """
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
        """Create a new collaboration request and return it"""
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
    """Serializer for offering collaboration"""
    id = serializers.IntegerField(read_only=True)
    offerers = StudentShortSerializer(many=True, read_only=True)

    class Meta:
        model = CollaborationRequest
        fields = ('id', 'offerers',)
    
    def update(self, instance, validated_data):
        """Add the logged student to the collaboration request's offerers"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            student = request.user.student

        if student == instance.applicant:
            raise serializers.ValidationError('You cannot offer collaboration in one of your collaboration requests')

        if student in instance.offerers.all():
            raise serializers.ValidationError('You\'ve already offered to collaborate on this collaboration request')

        instance.offerers.add(student)
        return instance