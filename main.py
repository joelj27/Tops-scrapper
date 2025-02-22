import requests
import json
from urllib.parse import quote
from nested_lookup import nested_lookup
import tqdm
from bs4 import BeautifulSoup
from concurrent.futures.thread import ThreadPoolExecutor

headers = {
      'Accept': '*/*',
      'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Origin': 'https://www.tops.co.th',
      'Referer': 'https://www.tops.co.th/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'cross-site',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
      'content-type': 'application/x-www-form-urlencoded',
      'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'x-algolia-api-key': '74c36eaa211b83d1a2575f9d7bdbf5dc',
      'x-algolia-application-id': 'L7MUX9U4CP'
    }

#Function to concordinate the catagory id for the payload
def get_cuid(sub_catagory):
    c_uid=""
    for index,i in enumerate(sub_catagory):
        if index+1 != len(sub_catagory):
            c_uid=c_uid+'category_uids:"{}" OR '.format(i)
        else:
            c_uid=c_uid+'category_uids:"{}" '.format(i)
    return c_uid
#Function to get the product data and the no of product in a catagory
def get_product(payload,Catagory):
    url = "https://l7mux9u4cp-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.5.1)%3B%20Browser%3B%20instantsearch.js%20(4.44.0)%3B%20JS%20Helper%20(3.10.0)"
    response = requests.request("POST", url, headers=headers, data=payload)
    j_data=json.loads(response.text)
    if Catagory=="Product_count":
        return j_data["results"][0]["nbPages"]
    elif Catagory=="Product":
        return [i["url_key"] for i in j_data["results"][0]["hits"]]
#Function to construc the paylod of differnrt catagory dynamic with the catagpry id
def get_payload(page,c_uid,key):
    if key=="OTOP":
        Payload = '{\"requests\":[{\"indexName\":\"tops_en_products_recommened_sort_order_desc\",\"params\":\"clickAnalytics=true&facets=%5B%22categories.level0%22%2C%22promotions.cluster_1.type%22%2C%22brand_name%22%5D&filters='+quote(c_uid)+'AND%20visibility_search%3D1%20AND%20visibility_catalog%3D1%20AND%20stock.CFR432.is_in_stock%3Atrue%20AND%20cluster%3Acluster_1&hitsPerPage=15&page='+page+'&maxValuesPerFacet=1000&ruleContexts=%5B%22promotion-otop-16jan-28feb-2025%22%5D&tagFilters=&facetFilters=%5B%22visibility_search%3A1%22%5D\"}]}'
    elif key=="OAT":
        Payload= '{\"requests\":[{\"indexName\":\"tops_en_products_recommened_sort_order_desc\",\"params\":\"clickAnalytics=true&facets=%5B%22categories.level0%22%2C%22promotions.cluster_1.type%22%2C%22brand_name%22%5D&filters='+quote(c_uid)+'AND%20visibility_search%3D1%20AND%20visibility_catalog%3D1%20AND%20stock.CFR432.is_in_stock%3Atrue%20AND%20cluster%3Acluster_1&hitsPerPage=15&page='+page+'&maxValuesPerFacet=1000&ruleContexts=%5B%22only-at-tops%22%5D&tagFilters=&facetFilters=%5B%22visibility_search%3A1%22%5D\"}]}'
    else:
        Payload='{"requests":[{"indexName":"tops_en_products_recommened_sort_order_desc","params":"clickAnalytics=true&facets=%5B%22categories.level2%22%2C%22brand_name%22%2C%22promotions.cluster_1.type%22%2C%22country_of_product%22%2C%22lifestyle_and_benefit%22%5D&filters='+quote(c_uid)+'AND%20visibility_search%3D1%20AND%20visibility_catalog%3D1%20AND%20stock.CFR432.is_in_stock%3Atrue%20AND%20cluster%3Acluster_1&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=15&maxValuesPerFacet=1000&page='+page+'&tagFilters=&facetFilters=%5B%22visibility_search%3A1%22%5D"}]}'
    return Payload
#Funtion to get the product data
def get_product_data(data):
    try:
        response=requests.get(data["url"],headers=headers)
        soup=BeautifulSoup(response.text,"html5lib")
        data["Product Name"]=soup.find("h1",class_="product-tile__name").text
        data["Product Images"]=[i.get("src") for i in soup.find("div",class_="product-Details-carousel swiper-wrapper").find_all("img")]
        try:
            data["Product Details"]=soup.find("div",class_="accordion-property").text.split(":")[-1].split("The product received may be subject to package modification and quantity from the manufacturer")[0].strip()
        except:
            data["Product Details"]=""
        url = "https://l7mux9u4cp-dsn.algolia.net/1/indexes/tops_en_products_recommened_sort_order_desc/{}?x-algolia-agent=Algolia%20for%20JavaScript%20(4.5.1)%3B%20Browser%3B%20instantsearch.js%20(4.44.0)%3B%20JS%20Helper%20(3.10.0)&attributesToRetrieve=%5B%22brand_name%22%2C%22categories%22%2C%22consumer_unit%22%2C%22discount_amount%22%2C%22final_price%22%2C%22image%22%2C%22marketplace_seller%22%2C%22name%22%2C%22price%22%2C%22sku%22%2C%22stock%22%2C%22type_id%22%2C%22url_key%22%2C%22visibility_catalog%22%2C%22gtm_data%22%2C%22promotions%22%2C%22product_badge%22%2C%22country_of_product%22%2C%22bundle_options%22%2C%22is_seasonal%22%5D".format(data["url"].split("-")[-1])
        response = requests.request("GET", url, headers=headers, data=payload)
        api_data=json.loads(response.text)
        data["Quantity "]=""
        data["Price"]=api_data["final_price"]["THB"]["cluster_1"]
        data["Barcode Number"]=api_data["sku"]
        try:
            data["Labels"]=api_data["product_badge"]["label"]
        except:
            data["Labels"]=None
        return data
    except Exception as e:
        print(e)
        with open('Error.txt', 'a') as file:
            file.write(data["url"]+"\n")
    

#Catagory name and the catagory ID
all_catagory_name_id={"OTOP":None,
"OAT":None,
"Fruits & Vegetables":"MzQ2NTQ0",
"Meat & Seafood":"MzQ2NjU1",
"Fresh Food & Bakery":"MzQ3NzU2",
"Pantry & Ingredients":"MzQ3OTg0",
"Snacks & Desserts":"MzQ2ODU2",
"Beverages":"MzQ4Mjk5",
"Health & Beauty Care":"MzQ2OTgy",
"Mom & Kids":"MzQ3MTk4",
"Household & Merit":"MzQ3OTgx",
"PetNme":"MzgwMzIw"}

print("Listing page sourcing started...")
data_dict={}
for key,value in all_catagory_name_id.items():
    print("Sourcing {} Page....".format(key))
    if value==None:
        c_uid=get_cuid(([i for i in list(all_catagory_name_id.values()) if i != None]))
    else:
        c_uid=get_cuid([value])
    page="1"
    payload=get_payload(page,c_uid,key)
    No_Of_pages=get_product(payload,"Product_count")
    all_product_url=[]
    for i in tqdm.tqdm(range(No_Of_pages)):
        payload=get_payload(str(i),c_uid,key)
        Product=get_product(payload,"Product")
        all_product_url.extend(["https://www.tops.co.th/en/"+i for i in Product])
    data_dict[key]=all_product_url
    # break
with open('Catagory.json'.format(key), 'w') as f:
        json.dump(data_dict, f)
data_dict=json.load(open('Catagory.json'))
    
print("Product page sourcing started...")
    
for key,value in data_dict.items():
    print("Sourcing Product {} Page....".format(key))
    dic_value=[{"url":i} for i in value]
    with ThreadPoolExecutor(max_workers=64) as exe:
        d=list(tqdm.tqdm(exe.map(get_product_data,dic_value),total=len(dic_value)))
    with open('{}.json'.format(key), 'w') as f:
        json.dump(dic_value, f)