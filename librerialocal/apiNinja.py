from ninja import NinjaAPI

import json
from django.core.serializers.json import DjangoJSONEncoder
from ninja.renderers import BaseRenderer

#Si queremos ver las vocáles con tilde, en lugar de su representación en código unicode (ej: ó en lugar de \u00f3) en la respuesta json, tenemos que hacer un objeto que la renderize a lenguaje humano:

class RenderizadorJSONpersonalizado(BaseRenderer):
    media_type = "application/json"
    json_encoder = DjangoJSONEncoder  # <-- Define el atributo aquí

    def render(self, request, data, response_status=None):
        return json.dumps(data, ensure_ascii=False, cls=self.json_encoder)

apiXXX = NinjaAPI(renderer=RenderizadorJSONpersonalizado())

#apiXXX = NinjaAPI()

#http://127.0.0.1:8000/api-ninja/saludar
@apiXXX.get("/saludar")
def hola(request): #En django ninja, request es reservado, no se puede usar un nombre de parámetro arbitrario.
    return "Hola mundo !!!"

#http://127.0.0.1:8000/api-ninja/operar_2_enteros?operacion=suma&x=5&y=10 Recuerde que antes del "?" no va "/"
@apiXXX.get("/operar_2_enteros")
def operar2enteros(request, operacion:str, x: int, y: int): 
    if operacion in ["suma", "resta"]:
        if operacion == "suma": return {"resultado de la suma": x + y}
        if operacion == "resta": return {"resultado de la resta": x - y}
    else: 
        return f"No proporcinó tipo de operación permitida (resta o suma) o la escribió mal ({operacion})."