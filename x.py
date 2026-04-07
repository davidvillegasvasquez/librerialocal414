#Cliente drf para biblioteca localfrom snippets.models import Snippet
#Abrir en la shell django: exec(open('x.py').read())
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()

serializer = SnippetSerializer(snippet)

print(f'data serializada: {serializer.data}')
print('')

content = JSONRenderer().render(serializer.data)

print(f'data renderizada a JSON: {content}')
print('')

#La deserialización es similar. Primero analizamos un flujo de datos y lo convertimos a tipos de datos nativos de Python...

import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = SnippetSerializer(data=data)
print(f'serializer.is_valid(): {serializer.is_valid()}')
print(f'serializer.validated_data: {serializer.validated_data}')
print('')
serializer.save()
#<Snippet: Snippet object>
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
print(f'serializer.data: {serializer.data}')
print('')
print(repr(serializer))

