# Robots Analysis for the Daily Pennsylvanian

The Daily Pennsylvanian's `robots.txt` file is available at
[https://www.thedp.com/robots.txt](https://www.thedp.com/robots.txt).

## Contents of the `robots.txt` file on March 4, 2025

```
User-agent: *
Crawl-delay: 10
Allow: /

User-agent: SemrushBot
Disallow: /
```

## Explanation  

The `robots.txt` file controls how web crawlers interact with The Daily Pennsylvanian's site:  

- `User-agent: *` applies to all crawlers.  
- `Crawl-delay: 10` enforces a 10-second wait between requests.  
- `Allow: /` permits full site access.  
- `User-agent: SemrushBot` specifically targets SemrushBot.  
- `Disallow: /` blocks SemrushBot from crawling any pages.  

This setup allows general indexing while restricting SemrushBot, likely to prevent competitive analysis.
