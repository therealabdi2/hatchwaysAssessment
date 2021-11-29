import requests
import requests_cache
from flask import Flask, jsonify, request

app = Flask(__name__)

# whenever you use requests, the response will be cached automatically.
requests_cache.install_cache(cache_name='hatchways_cache', backend='sqlite', expire_after=180)

# The Api used to fetch blog data
HATCHWAYS_URL = "https://api.hatchways.io/assessment/blog/posts"


# Route 1
@app.route('/api/ping')
def get_response():
    return jsonify({"success": True}), 200


# Route 2 to get posts
# http://127.0.0.1:5000/api/posts/?tags=history,tech,health,politics,science,design,startups,culture
@app.route('/api/posts/')
def get_posts():
    # getting the values from passed parameter
    tags = request.args.get("tags")
    if tags is None or tags == "":
        return jsonify({"error": "Tags Parameter is required"}), 400

    # if no parameter is given then set a default value for sortBy and direction
    sortBy = request.args.get("sortBy")
    if sortBy is None or sortBy == "":
        sortBy = "id"

    direction = request.args.get("direction")
    if direction is None or direction == "":
        direction = "asc"

    # Call the api for every tag in a list i.e tags = ["history", "tech"]
    tags = tags.split(",")

    # Add all posts and return the response as JSON data
    result = {'posts': []}
    for tag in tags:
        hatchways_params = {
            "tag": tag,
        }
        # Get all posts related to the specific tag
        posts = requests.get(url=HATCHWAYS_URL, params=hatchways_params).json()['posts']

        # Combines all post into one list of dictionaries
        for post in posts:
            result['posts'].append(post)

    # Remove duplicates with the use of list comprehension and enumerate
    result['posts'] = [i for n, i in enumerate(result['posts']) if i not in result['posts'][n + 1:]]

    # used for sorting logic, reverse sorts in asc if False desc if TRUE
    if direction == "asc":
        reverse = False
    elif direction == "desc":
        reverse = True
    else:
        return jsonify({"error": "direction parameter is invalid"}), 400

    # we will take a list of posts and sort them by the given key
    list_to_be_sorted = result["posts"]
    try:
        # The sorted() function takes a key = parameter to sort by
        sortedlist = sorted(list_to_be_sorted, key=lambda k: k[sortBy], reverse=reverse)
    except KeyError:
        # if invalid key is given we sent a 400 error back
        return jsonify({"error": "sortBy parameter is invalid"}), 400

    # add the sorted list back to dictionary and serve it as JSON data
    final_result = {'posts': []}
    for post in sortedlist:
        final_result['posts'].append(post)

    return jsonify(final_result), 200


if __name__ == '__main__':
    app.run(debug=True)
