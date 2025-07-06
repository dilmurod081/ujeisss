from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Player, Message

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if Player.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=409)

        player = Player.objects.create(username=username, password=password)
        return JsonResponse({'message': 'Registration successful'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            player = Player.objects.get(username=username)
            if player.password == password:
                messages = list(player.messages.all().values('content'))
                return JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'username': player.username,
                        'coins': player.coins,
                        'achievementSent': player.achievement_sent,
                        'messages': [msg['content'] for msg in messages]
                    }
                })
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=401)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_user_data(request, username):
    if request.method == 'POST':
        try:
            player = Player.objects.get(username=username)
            data = json.loads(request.body)
            player.coins = data.get('coins', player.coins)
            player.achievement_sent = data.get('achievementSent', player.achievement_sent)
            player.save()
            return JsonResponse({'message': f'User {username} updated successfully'})
        except Player.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all_users(request):
    if request.method == 'GET':
        players = Player.objects.all().values_list('username', flat=True)
        return JsonResponse(list(players), safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)