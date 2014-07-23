from surfice.models import *
from rest_framework import serializers

class SurfSerializer(serializers.ModelSerializer):
	""" Serialize a surf and its components
		
	"""
	
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Surf

class StatusSerializer(serializers.ModelSerializer):
	""" Serialize a status and its components
	"""
	
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Status

class SurficeSerializer(serializers.ModelSerializer):
	""" Serialize a surfice and its components
	"""
	
	surfs = SurfSerializer(many=True)
	status = StatusSerializer()
	
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Surfice

class EventSerializer(serializers.ModelSerializer):
	""" Serialize an event and its components
		
		Includes status and surfice serialized as well
	"""
	
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
	""" Serialize a ding and its components
		
		Includes status and surfice serializers also
	"""
	
	status = StatusSerializer()
	surfice = SurficeSerializer()
	data = serializers.SerializerMethodField('get_data_field')
	
	# To get data, we have to go through the method or else
	# it is not formatted correctly
	def get_data_field(self, obj):
		return obj.data
	
	class Meta:
		model = Ding
