from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from rest_framework import serializers
from core.models import Student, Degree, Competence
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User"""
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5, 'max_length': 32}}
    
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class DegreeSerializer(serializers.ModelSerializer):
    """Serializer for Degree"""
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
    """Serializer for Competence"""
    class Meta:
        model = Competence
        fields = ('name',)


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student"""
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for authentication token"""
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
    