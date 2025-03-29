import os

def main():
    #find every file first
    files = os.listdir()
    print(files)
    url_set = set()
    if "urls.txt" in files:
        os.remove("urls.txt")
    final = open("urls.txt", "a+")   
    for file in files:
        if file.endswith(".txt"):
            with open(file, "r") as f:
                urls = f.read().split()
            for url in urls:
                url_set.add(url)
    final.write("\n".join(url_set) + "\n")


if __name__ == "__main__":
    main()