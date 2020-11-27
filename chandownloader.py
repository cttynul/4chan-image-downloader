import requests, re, os, json, sys, getopt
import urllib.request

def downloader(url, thread_title, filename):
    print("Processing: " + filename)
    new_folder = re.sub('[^\w\-_\. ]', '_', os.path.join(os.getcwd(), thread_title))
    if not os.path.exists(new_folder): os.makedirs(new_folder)
    full_path = os.path.join(new_folder, filename)
    r = requests.get('http:' + url, allow_redirects=True)
    open(full_path, 'wb').write(r.content)

def without_API(url):
    pattern = r'File\:[^\/]+([^"]+)[^>]+>([^<]+)'
    if "4chan" in url: response = requests.get(url)
    else: response = False
    if response:
        text = response.text
        thread_title = re.findall(r'<title>([^<]+)<\/title>', text)[0]
        matches = re.findall(pattern, text)
        for url, filename in matches:
            try: downloader(url, thread_title, filename)
            except: print("Something Happen! Cannot process " + filename)
        print("Done!")
    else:
        print("WTF!? Is this a legit input according to you? " + url)
        exit(1)

def with_API(url):
    if "4chan" not in url:
        print("WTF!? Is this a legit input according to you? " + url)
        exit(1) 
    splitted = url.split("/")
    url_api = "https://a.4cdn.org/" + splitted[-3] + "/thread/" + splitted[-1] + ".json"
    dump = urllib.request.urlopen(url_api)
    data = json.loads(dump.read().decode())
    for post in data["posts"]:
        try:
            try: theard_title = data["posts"][0]["sub"]
            except: theard_title = data["posts"][0]["com"] 
            if "filename" in post: downloader(url="//is2.4chan.org/" + splitted[-3] + "/" + str(post["tim"]) + post["ext"], thread_title=theard_title, filename=post["filename"] + post["ext"])
        else: print("Something Happen! No verbosity here.")

def exit_and_print(name):
    print(name + " -u|--url <thread_url> [-a|--api <default=y|nope>]")
    sys.exit()

def print_logo():
    print(" ▲")
    print("▲ ▲")
    print("\nnewfag can't triforce\n")

def main(argv, pyname):
    print_logo()
    api = None
    url = None
    try: opts, args = getopt.getopt(argv,"u:a:",["url=","api="])
    except getopt.GetoptError: exit_and_print(name=pyname)
    for opt, arg in opts:
        if opt == '-h': exit_and_print()
        elif opt in ("-u", "--url"): url = arg
        elif opt in ("-a", "--api"): api = arg
    
    if url is None:
        exit_and_print(name=pyname)
    elif api == "nope":
        without_API(url)
    else:
        with_API(url)
    
if __name__ == "__main__":
    main(sys.argv[1:], sys.argv[0])
