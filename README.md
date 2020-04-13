# tu-easter

In April 2020 the TU Delft TPM Faculty organized a digital easter egg hunt. The full description of the challenge can be found below. This repository contains a **quick and dirty** web scraper that found the eggs for me, and provided a list of possible solutions for me to pick the most sensible one from. This script was mashed together in one sitting just for fun. 

The scraper tracks two Sets of URLs: one for _visited_ pages, and one for _remaining_ pages. Sets are chosen because of the large amount of membership tests. The scraper is given one URL to add to `remaining` before starting. Page URLs in `remaining` are processed sequentially. When processing a URL it is removed from `remaining`, the page source is loaded and the URL is added to `visited`. Links to other pages on the faculty page are identified with regex and added to `remaining` if not already in `visited`. The easter eggs are also identified with regex based on a common file path. When discovered, the egg's letter is identified from the file name. The letter and the url the egg was found on are stored in a list of `(letter, url)` tuples. 

After all letters are collected, their frequencies are stored in a dict. A word list is loaded and filtered down to only include words of the right lengths with letters from our egg hunt. A hideous three-layer for-loop iteratively combines words from the word list and counts if they are a valid answer with respect to the available letters. The output is a list of all valid three-word permutations from the word list. This list can easily be skimmed through manually to find the only sensible entry. 

There are two reasons I consider this approach ethical, even with a prize. For starters, the eggs were easy enough to find manually: this approach didn't give a substantial advantage. Secondly, this is a technical university: it would be a shame if we're  expected not to apply the knowledge we obtain :)

---

# Challenge Description

The challenge was introduced in the following email:

> Dear faculty staff and students,
>
> I'm sure I'm not just speaking for myself when I say I'm really enjoying the arrival of spring. The warmth of the sun. The fresh scent of green grass and new leaves. Everything in bloom. We have a nice long Easter weekend ahead of us. A weekend where we can take a step back, rest and enjoy spring.
>
> [...]
>
> **TPM easter egg challenge**  
> But now the Easter weekend is here. Time to relax! We devised the TPM easter egg challenge especially for this purpose. We have hidden 17 Easter eggs on our website (https://www.tudelft.nl/tbm/). There is a letter on every Easter egg. Together, the letters form an English-language phrase that fits these dots:
>
> `======     ===    ========`
>
> Among the good entries, we raffle [a prize]. You can send in your solution until April 14, 2020 to [redacted], stating "TPM easter egg challenge".
>
> I wish you all a wonderfully relaxed Easter weekend.
>
> With kind regards,
>
> [Faculty Staff]
