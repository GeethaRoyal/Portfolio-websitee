from imdb.models import *
from django.core.exceptions import ObjectDoesNotExist

def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
	 for actor in actors_list:
	 	Actor.objects.create(actor_id=actor["actor_id"],name=actor["name"])
	 	
	 for directors in directors_list:
	 	Director.objects.create(name=directors)
	 
	 for movies in movies_list:
	 	Movie.objects.create(movie_id=movies["movie_id"],name=movies["name"],
	 	box_office_collection_in_crores=movies["box_office_collection_in_crores"],
	 	release_date=movies["release_date"],
	 	director=Director.objects.get(name=movies['director_name']))
	 	for actor in movies['actors']:
	 		Cast.objects.create(is_debut_movie=actor["is_debut_movie"],
	 		actor=Actor.objects.get(actor_id=actor['actor_id']),
	 		movie=Movie.objects.get(movie_id=movies['movie_id']),role=actor['role'])
	 	
	 for movies in movie_rating_list:   
	 	ids=Movie.objects.get(movie_id=movies['movie_id'])
	 	Rating.objects.create(movie=ids,rating_one_count=movies["rating_one_count"],
	 	rating_two_count=movies["rating_two_count"],rating_three_count=movies["rating_three_count"],
	 	rating_four_count=movies["rating_four_count"],rating_five_count=movies["rating_five_count"])
	 
	 
def get_no_of_distinct_movies_actor_acted(actor_id):     
	return Movie.objects.filter(actors__actor_id=actor_id).distinct().count()
   
def get_movies_directed_by_director(director_obj):
	return list(director_obj.movie_set.all())

def get_average_rating_of_movie(movie_obj):
	try:
		rate=Rating.objects.get(movie=movie_obj)
		one,two,three,four,five=rate.rating_one_count,rate.rating_two_count,rate.rating_three_count,rate.rating_four_count,rate.rating_five_count
		sum_of_rate=one+two*2+three*3+four*4+five*5
		count=one+two+three+four+five
		return sum_of_rate/count
	except ObjectDoesNotExist:
		return 0
	except ZeroDivisionError:
		return 0
	
def delete_movie_rating(movie_obj):
	try:
		rate=Rating.objects.get(movie=movie_obj)
	except ObjectDoesNotExist:
		return 0
	rate.delete()
	
def get_all_actor_objects_acted_in_given_movies(movie_objs):
	return list(Actor.objects.filter(movie__in = movie_objs).distinct())
	
def update_director_for_given_movie(movie_obj, director_obj):
    movie_obj.director=director_obj
    movie_obj.save()
             
def get_distinct_movies_acted_by_actor_whose_name_contains_john():
	return Movie.objects.filter(actors__name__contains='john').distinct()
	
def remove_all_actors_from_given_movie(movie_obj):
	movie_obj.actors.clear()
	
def get_all_rating_objects_for_given_movies(movie_objs):
	return Rating.objects.filter(movie__in=movie_objs)
	
	
	
	
from django.db import models
       
# Create your models here.
class Director(models.Model):
	name = models.CharField(max_length=200,unique = True)
	
class Actor(models.Model):
	actor_id = models.CharField(max_length=100,primary_key=True)
	name = models.CharField(max_length = 100)
	
class Movie(models.Model):
	name = models.CharField(max_length=100)
	movie_id = models.CharField(max_length = 100,primary_key= True)
	release_date = models.DateField()
	box_office_collection_in_crores = models.FloatField()
	director = models.ForeignKey(Director,on_delete = models.CASCADE)
	actors=models.ManyToManyField(Actor,through='Cast')

class Cast(models.Model):
	role = models.CharField(max_length = 50)
	actor=models.ForeignKey(Actor,on_delete = models.CASCADE)
	movie=models.ForeignKey(Movie,on_delete = models.CASCADE)
	is_debut_movie= models.BooleanField(default = False)

class  Rating(models.Model):
	movie = models.OneToOneField(Movie,on_delete = models.CASCADE)
	rating_one_count = models.IntegerField(default = 0)
	rating_two_count = models.IntegerField(default = 0)     
	rating_three_count = models.IntegerField(default = 0)
	rating_four_count = models.IntegerField(default = 0)
	rating_five_count = models.IntegerField(default = 0)   