from webscrapper import WebScrapper

rankings = WebScrapper.getRankings()
distinctNames = WebScrapper.getDistinctNames(rankings)
wikiLinksAndNames = WebScrapper.getWikiLinks(rankings[6], distinctNames)

wikiLinksAndNames[0].remove('/wiki/Alexei_Papin')
wikiLinksAndNames[0].remove('/wiki/Hugo_Centeno_Jr.')
wikiLinksAndNames[0].remove('/wiki/Denys_Berinchyk')
wikiLinksAndNames[0].remove('/wiki/Tervel_Pulev')
            
fights = WebScrapper.getUpcomingFights(wikiLinksAndNames[0], wikiLinksAndNames[1])

for f in fights: print(f)
print(len(fights))







    