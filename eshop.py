import requests
import json
import time
import urllib.parse

base_address = 'https://u3b6gr4ua3-dsn.algolia.net'
relative_path = '/1/indexes/*/queries'
query_strings = ('?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)'
                '%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&'
                'x-algolia-application-id=U3B6GR4UA3&x-algolia-api-key=9a20'
                'c93440cf63cf1a7008d75f7438bf')
url = "{0}{1}{2}".format(base_address, relative_path, query_strings)

headers = {
'Content-Type': 'application/x-www-form-urlencoded',
'Accept': 'application/json'
}

categories = ('Action', 'Adventure', 'Application', 'Education', 
                'Fitness', 'Indie', 'Music', 'Party', 'Puzzle', 
                'Racing', 'Role-Playing', 'Simulation', 'Sports', 
                'Strategy')

price_ranges = ('Free to start', '$0 - $4.99', '$5 - $9.99', 
                '$10 - $19.99', '$20 - $39.99','$40+')

def main():
    for c in categories:
        json_file_name = "./{0}.json".format(c)
        json_file = open(json_file_name,"w")
        data_to_json = []
        for p in price_ranges:
            end_pagination = False
            page = 0
            while end_pagination is False:
                post_payload = get_post_payload(c, p, page)

                json_response = (requests.request("POST", url, 
                                headers=headers, 
                                data = post_payload)).text.encode('utf8')
                json_decoded = json.loads(json_response)

                if not json_decoded['results'][0]['hits']:
                    end_pagination = True
                else:
                    print("Category: {0}, Price: {1}, " \
                    "Page: {2} , Games Found: {3}" \
                    .format(c, p, str(page), 
                    str(len(json_decoded['results'][0]['hits']))))
                    
                    data_to_json.append(json_decoded['results'][0]['hits'])

                    page = page + 1
        json_file.write(json.dumps(data_to_json))
        json_file.close()

def get_post_payload(category, price, page):
    return "{\"requests\":[{\"indexName\":\"noa_aem_game_en_us\"" \
    ",\"params\":\"query=&hitsPerPage=42&maxValuesPerFacet=30" \
    "&page=" \
    + str(page) + \
    "&facets=%5B%22generalFilters%22%2C%22platform%22%2" \
    "C%22availability%22%2C%22categories%22%2C%22filterShops%2" \
    "2%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRan" \
    "ge%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&f" \
    "acetFilters=%5B%5B%22priceRange%3A" \
    + urllib.parse.quote(price) + \
    "%22%5D" \
    "%2C%5B%22categories%3A" \
    + category + \
    "%22%5D%5D\"},{\"indexName\":" \
    "\"noa_aem_game_en_us\",\"params\":\"query=&hitsPerPage=1" \
    "&maxValuesPerFacet=30&page=" \
    + str(page) + \
    "&attributesToRetrieve=%5B%5D" \
    "&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D" \
    "&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22cat" \
    "egories%3A" \
    + category + \
    "%22%5D%5D\"},{\"indexName\":\"noa_aem_ga" \
    "me_en_us\",\"params\":\"query=&hitsPerPage=1&maxValuesPe" \
    "rFacet=30&page=" \
    + str(page) + \
    "&attributesToRetrieve=%5B%5D&attributesT" \
    "oHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=" \
    "&facets=categories&facetFilters=%5B%5B%22priceRange%3AFr" \
    "ee%20to%20start%22%5D%5D\"}]}"

if __name__ == '__main__':
    main()