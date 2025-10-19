from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
# Create your views here.
movies = []
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    
    # Calculate average ratings for each movie
    movies_with_ratings = []
    for movie in movies:
        reviews = Review.objects.filter(movie=movie)
        if reviews.exists():
            avg_rating = sum(review.rating for review in reviews) / reviews.count()
            movie.avg_rating = round(avg_rating, 1)
            movie.total_ratings = reviews.count()
        else:
            movie.avg_rating = 0
            movie.total_ratings = 0
        movies_with_ratings.append(movie)
    
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies_with_ratings
    return render(request, 'movies/index.html',
                  {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    
    # Calculate average rating
    if reviews.exists():
        average_rating = sum(review.rating for review in reviews) / reviews.count()
        template_data['average_rating'] = round(average_rating, 1)
        template_data['total_ratings'] = reviews.count()
    else:
        template_data['average_rating'] = 0
        template_data['total_ratings'] = 0
    
    # Check if current user has already rated this movie
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(movie=movie, user=request.user).first()
    template_data['user_review'] = user_review
    
    return render(request, 'movies/show.html',
                  {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        
        # Check if user already has a review for this movie
        existing_review = Review.objects.filter(movie=movie, user=request.user).first()
        
        if existing_review:
            # Update existing review
            existing_review.rating = rating
            if comment:
                existing_review.comment = comment
            existing_review.save()
        else:
            # Create new review
            review = Review()
            review.rating = rating
            review.comment = comment if comment else None
            review.movie = movie
            review.user = request.user
            review.save()
        
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        review = Review.objects.get(id=review_id)
        review.rating = request.POST.get('rating', review.rating)
        review.comment = request.POST.get('comment', '')
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)