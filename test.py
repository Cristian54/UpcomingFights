from webscrapper import WebScrapper

rankings = WebScrapper.getRankings()
distinctNames = WebScrapper.getDistinctNames(rankings)
fightersWikiLinks = WebScrapper.getWikiLinks(rankings[6], distinctNames)