from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Lightweight health check for uptime pingers and Render's health checks.
# Returns 200 without touching the database so it stays cheap to call often.
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})
