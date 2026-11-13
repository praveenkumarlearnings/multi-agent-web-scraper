# from tools import discover_urls

# result = discover_urls.run(
#     "https://quotes.toscrape.com/"
# )

# print(result)



from tools import discover_urls, extract_content

# Test Tool 1: Discover URLs
urls = discover_urls.run(
    "https://quotes.toscrape.com/"
)

print("DISCOVERED URLS:")
print(urls)


# Test Tool 2: Extract Website Content
content = extract_content.run(
    "https://quotes.toscrape.com/author/Jane-Austen"
)

print("\nEXTRACTED CONTENT:")
print(content)

