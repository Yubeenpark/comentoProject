
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe

import json
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    
    logger.debug('Come into chat room number={} by username={}, id={}. '.format(room_name,request.user.username,request.user.id))
    return render(request, 'chat/chat.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username' :mark_safe(json.dumps(request.user.username)),
        
    })
