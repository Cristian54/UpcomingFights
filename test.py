from webscrapper import WebScrapper

rankings = WebScrapper.getRankings()
distinctNames = WebScrapper.getDistinctNames(rankings)
wikiLinksAndNames = WebScrapper.getWikiLinks(rankings[6], distinctNames)
WebScrapper.getUpcomingFights(wikiLinksAndNames[0], wikiLinksAndNames[1])