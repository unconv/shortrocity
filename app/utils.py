
def download_html_from_url(url):
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Now 'html_content' contains the HTML of the webpage
        # print(html_content)
        with open("./data/file.html" , "w") as f:
            f.write(html_content)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


def load_html_text(url:str="https://www.mcdonalds.com/us/en-us/about-our-food.html") :
    """
    accepts a link to an html website 
    returns : A Document langchain object with text scrapped 
    """
    from langchain.document_loaders import BSHTMLLoader , UnstructuredHTMLLoader
    download_html_from_url(url)
    loader = UnstructuredHTMLLoader(file_path="./data/file.html")
    data = loader.load()
    # print(f"type of object : {type(data)} & data is : {data}")
    with open("./data/file.txt" , "w") as f:
        f.write(data[0].page_content)
    return data[0].page_content

# load_html_text()

# load_html_text(url="https://www.mcdonalds.com/us/en-us/about-our-food.html")

def clean(data:str)->list :
    l=[]
    data = data.split("\n")
    for d in data : 
        cleaned = d.strip().replace('"' , '').replace("\n",'').replace('[' ,'').replace(']','')
        l.append(cleaned)
        print(cleaned)
    print(l)
    return l 

def create_dict_pairs(text:list , images:list) -> dict :
    l = []
    for tex , img in zip(text,images):
        i={}
        if len(tex) > 0  and len(img) > 0 : 
            i["text"] , i["image"]= tex , img 
            l.append(i)
    print(l)
    return l
        