# TU-easter.py
# Find all easter eggs for the 2020 TPM easter challenge

from collections import defaultdict
import re
from string import ascii_letters
from typing import DefaultDict, Dict, List, Set, Tuple
import requests


visited: Set[str] = set() # collection of visited urls
remaining: Set[str] = set() # collection of discovered urls that need visiting
eggs: List[Tuple[str, str]] = [] # collection (letter, url) tuples


def loadPage(url: str) -> str:
    """Load the page data for provided URL and track the visit."""
    r = requests.get(url)
    page_content = r.text

    visited.add(url)

    if r.status_code != 200:
        print(f"Error {r.status_code} when loading url {url}!")
        return ""

    return page_content


def makeHardLink(url: str, prefix="https://www.tudelft.nl") -> str:
    if url[0] == "/":
        index_params = url.find("?")
        if index_params >= 0:
            url = url[:index_params]
        return prefix + url   
    return ""


def findEgg(pageSource: str, url: str):
    """Find eggs, if any, in the provided page source. Assume max 1 egg per page."""

    # TODO: Clean up the regex to a single, all-encompassing pattern.
    regex = r"faculteit\/Afdelingen\/Communicatie\/.\.png"
    match = re.search(regex, pageSource)

    # if no match, find duplicates using their naming scheme
    if not match:
        regex = r"faculteit\/Afdelingen\/Communicatie\/.-\d\.png"
        match = re.search(regex, pageSource)

    # if no match, find special characters using %-codes
    if not match:
        regex = r"faculteit\/Afdelingen\/Communicatie\/%..\.png"
        match = re.search(regex, pageSource)

    if match:
        egg = match.group(0)[-5] # set egg to character before file extension

        # catch letter repeats in format x-2.png
        if egg not in ascii_letters:
            egg = match.group(0)[-7]

        # catch special chars in %hex.png from the html encoding
        if egg == "%":
            egg_hex_str = match.group(0)[-6:-4]
            egg = chr(int(egg_hex_str, 16))

        eggs.append((egg, url))
    

def findLinks(pageSource: str):
    """Find links to other pages on the TPM website, and add unvisited ones to the to-do list."""
    
    link_regex = r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\1"
    # Match all link targets in pageSource
    matches = re.findall(link_regex, pageSource)
    
    found_urls = {match for _, match in matches if match[0:5] == "/tbm/"}

    for url in found_urls:
        full_url = makeHardLink(url)
        
        # if url not in visited, add to remaining
        if full_url not in visited and full_url:
            remaining.add(full_url)


def scrape(start_url: str):
    """
    Starting with the input URL, read pages, search for links to other pages, and read page to discover egg images in the source code.
    Code is interrupted if all 17 eggs are found. 
    """

    remaining.add(start_url)

    # While we have pages to visit
    while len(remaining):
        # Get any url from our set
        url = remaining.pop()
        print(f"Processing {url}")

        # assign url to visited
        visited.add(url)

        # Load the page
        page_content = loadPage(url)

        # skip page if something goes wrong
        if page_content == "":
            print(f"Skipping {url} ...")
            continue

        # find eggs
        findEgg(page_content, url)

        if len(eggs) == 17:
            break

        # find links
        findLinks(page_content)

        print(f"Remaining stack: {len(remaining)}, eggs: {len(eggs)} - {[x for x,_ in eggs ]}")


scrape("https://www.tudelft.nl/tbm/")


print("\n\n\n#########################################\n# Results:\n")
for letter, url in eggs:
   print(f"{letter} found at {url}")

print("\n\nAll letters: ", [egg for egg, _ in eggs])


###############################################
# Solve puzzle based on discovered letters


# TODO: Better word list. This one contains really strange entries.
# TODO: Download and save if missing, otherwise load locally.
word_list_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
all_letters = ["S", "T", "N", "E", "G", "D", "A", "T", "S", "R", "S", "A", "I", "R", "H", "P"]
word_lengths = (6, 3, 7)


def toLetterCount(word: str) -> defaultdict:
    letter_counts: DefaultDict[str, int] = defaultdict(int)
    
    for letter in list(word):
        letter_counts[letter.lower()] += 1
    
    return letter_counts


# This is a monster.
def bruteForceUnscramble(letters: List[str], lengths: Tuple[int, int, int], affix: str):
    # make dict of letter appearences
    letters = [c.lower() for c in letters]
    letter_limits = toLetterCount("".join(all_letters))

    # make set for quick member testing
    letter_set = set(letters)

    # prepare dict with word lengths as keys and word lists as value
    word_list = requests.get(word_list_url).text.splitlines()
    words: Dict[int, List[str]] = {n: [] for n in word_lengths}
        
    # select only words from word list of the proper length, with no impossible letters
    for word in word_list:
        if len(word) not in lengths:
            continue

        if len(set(list(word)) - letter_set) != 0:
            continue

        words[len(word)].append(word)

    # Overwrite 3-length words because those in the list are silly
    words[3] = ["and", "the", "has"]


    # nested for madness!
    for w1 in words[lengths[0]]:
        # count longest word
        w1_count = toLetterCount(w1)
        valid = True
        for c in letter_limits:
            if w1_count[c] > letter_limits[c]:
                valid = False
                break
        
        # skip to next w3 if invalid
        if not valid:
            continue

        for w2 in words[lengths[1]]:
            # count w1 and w3 together
            w1w2_count = toLetterCount(w1 + w2)

            valid = True
            for c in letter_limits:
                if w1w2_count[c] > letter_limits[c]:
                    valid = False
                    break
            
            # next w1 if the combination of w3 and w1 is invalid
            if not valid:
                continue

            
            # w3 and w1 are valid, find a w2 to finish up
            for w3 in words[lengths[2]]:
                # Count if w1 and w3 together are still valid
                all_count = toLetterCount(w1+w2+w3)

                valid = True
                for c in letter_limits:
                    if all_count[c] > letter_limits[c]:
                        valid = False
                        break
                
                if not valid:
                    continue

                print(f"{w1} {w2} {w3}{affix}") 


# bruteForceUnscramble(all_letters, word_lengths, "!")
# spring has started!