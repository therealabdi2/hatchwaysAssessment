import asyncio
import time

import aiohttp

posts = {
    'posts': None
}

HATCHWAYS_URL = "https://api.hatchways.io/assessment/blog/posts"

tags = ['history', 'tech', 'health', 'politics', 'science', 'design', 'startups', 'culture']

# start_time = time.time()
# result1 = {'posts': []}
# for tag in tags:
#     hatchways_params = {
#         "tag": tag,
#     }
#     # Get all posts related to the specific tag
#     posts = requests.get(url=HATCHWAYS_URL, params=hatchways_params).json()['posts']
#
#     # Combines all post into one list of dictionaries
#     for post in posts:
#         result1['posts'].append(post)
#
# print(result1)
# print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
results = []


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for tag in tags:
            task = asyncio.ensure_future(get_data(session, tag))
            tasks.append(task)

        await asyncio.gather(*tasks)


async def get_data(session, tag):
    url = f"https://api.hatchways.io/assessment/blog/posts?tag={tag}"
    async with session.get(url) as response:
        result_data = await response.json()
        results.append(result_data['posts'])


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

finalResult = []
for result in results:
    finalResult += result

# remove duplicates
finalResult = [i for n, i in enumerate(finalResult) if i not in finalResult[n + 1:]]

list_to_be_sorted = finalResult
sortedlist = sorted(list_to_be_sorted, key=lambda k: k['id'], reverse=False)

posts['posts'] = sortedlist
print(posts)

print("--- %s seconds ---" % (time.time() - start_time))
