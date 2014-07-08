from surfice.models import *
from rest_framework import serializers

class SurfSerializer(serializers.ModelSerializer):
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Surf

class StatusSerializer(serializers.ModelSerializer):
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Status

class SurficeSerializer(serializers.ModelSerializer):
	surf = SurfSerializer(many=False)
	status = StatusSerializer()
	
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Surfice

class EventSerializer(serializers.ModelSerializer):
	status = StatusSerializer()
	surfice = SurficeSerializer()
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Event

class DingSerializer(serializers.ModelSerializer):
	status = StatusSerializer()
	surfice = SurficeSerializer()
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Event
		