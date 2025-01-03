# yourapp/context_processors.py
def add_custom_variable(request):
    return {
        'custom_variable': 'カスタムデータ',
    }
