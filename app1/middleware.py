# yourapp/middleware.py
class AddCustomDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.custom_variableが既に設定されていない場合のみ False を設定
        if not hasattr(request, 'AI_chat'):
            request.AI_chat = False

        response = self.get_response(request)
        return response
