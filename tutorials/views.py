from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view

from .models import Comment, User, BlogPost, Tutorial
# Create your views here.

def blogs_view(request):
    han_solo = User('mongoblogger@reallycoolmongostuff.com', 'Han', 'Solo').save()
    chewbacca = User(
        'someoneelse@reallycoolmongostuff.com', 'Chewbacca', 'Thomas').save()
    
    BlogPost(
        # Since this is a ReferenceField, we had to save han_solo first.
        author=han_solo,
        title="Five Crazy Health Foods Jabba Eats.",
        content="...",
        tags=['alien health', 'slideshow', 'jabba', 'huts'],
        comments=[
            Comment(author=chewbacca, body='Rrrrrrrrrrrrrrrr!', vote_score=42)
        ]
    ).save()

    slideshows = BlogPost.objects.raw({'tags':'slideshow'})

    print(slideshows.only('title'))
    # print(slideshow_titles.first().title)
    print(slideshows)
    return HttpResponse(slideshows.values())


# drf-api mongo
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        title = request.GET.get('title', None)
        print(request.GET)
        print(title)
        if title is not None:
            tutorials = tutorials.filter(titler__icontains=title)
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False) 
        
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        tutorial = Tutorial.objects.get(pk=pk)
# get req
        if request.method == 'GET':
            print(tutorial)
            tutorial_serializer = TutorialSerializer(tutorial)
            print(tutorial_serializer.data)
            return JsonResponse(tutorial_serializer.data)
# update req
        elif request.method == 'PUT':
            tutorial_data = JSONParser.parse(request)
            tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
            if tutorial_serializer.is_valid():
                tutorial_serializer.save() 
                return JsonResponse(tutorial_serializer.data) 
            return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            tutorial.delete()
            return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

 
    # GET / PUT / DELETE tutorial
    

@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)