from django.shortcuts import render 
from django.http import JsonResponse 
from openai import OpenAI
import os


api_key = os.environ.get('sk--50')
if api_key is None:
    raise ValueError("API key is not set in the environment variables.")

client = OpenAI(api_key=api_key)

def get_completion(prompt): 
	print(prompt) 
	query = OpenAI().Completion.create( 
		engine="text-davinci-003", 
		prompt=prompt, 
		max_tokens=1024, 
		n=1, 
		stop=None, 
		temperature=0.5, 
	) 
	response = query.choices[0].text 
	print(response) 
	return response 


def query_view(request): 
	if request.method == 'POST': 
		prompt = request.POST.get('prompt') 
		response = get_completion(prompt) 
		return JsonResponse({'response': response}) 
	return render(request, 'index.html') 
