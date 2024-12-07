from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from . import translate, util


def index(request):
    context = {
        "title": "Braille",
    }
    return render(request, "braille/index.html", context)


def back_translate(request):
    if not util.is_ajax(request):
        return HttpResponseBadRequest("Invalid request: Ajax only.")
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request: GET only.")
    input = request.GET.get("input", "")
    print(f"Translating {input}...")
    output_lines = translate.braille_to_print(["en-ueb-g2.ctb"], input)
    if output_lines is None:
        print("Failed.")
        response = {"error": "Translation failed."}
        return JsonResponse(response, status=400)
    output = util.paragraphize(output_lines)
    response = {"translation": output}
    return JsonResponse(response)
