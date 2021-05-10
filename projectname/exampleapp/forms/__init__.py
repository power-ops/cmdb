try:  # 增加try的原因是form里有queryset，会导致makemigration失败
    from .example import ExampleForm
except:
    pass
