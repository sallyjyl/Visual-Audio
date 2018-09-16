
import requests


def search_for_image(input_keyword):
	search_query = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCVPDYrTm2h_keElXO1iAW-PW5RAlujEtg&cx=017480567514037437480%3Akvmd1lv2ahm&q=" + str(input_keyword) + "&searchType=image&fileType=jpg&imgSize=medium&num=1"
	# r = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyCVPDYrTm2h_keElXO1iAW-PW5RAlujEtg&cx=017480567514037437480%3Akvmd1lv2ahm&q=flower&searchType=image&fileType=jpg&imgSize=medium&num=1")
	r = requests.get(search_query)
	# print(r.status_code)
	# print(r.json())

	intermediate = r.json()


	return intermediate["items"][0]["link"]
	# print(intermediate["items"][0]["link"])

# "https://www.googleapis.com/customsearch/v1?key=AIzaSyCVPDYrTm2h_keElXO1iAW-PW5RAlujEtg&cx=017480567514037437480%3Akvmd1lv2ahm&q=flower&searchType=image&fileType=jpg&imgSize=medium"
print(search_for_image("flower"))