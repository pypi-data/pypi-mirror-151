# Scrapy Demo Cloudwatch Log

Adds a log line that is easy to parse with Cloudwatch filters to create a useful
metric. To enable:

```
EXTENSIONS = {
    'scrapy_demo_cloudwatch_log.DemoLogger': 100
}
```

Then you can use this filter expression: `{ $.eventType = "ScrapyCrawlSummary" }`.
It creates the demo metric `$.item_scraped_count`.
The `$.spider` can be used as a dimension.

Source code in [Github](https://github.com/scalingexcellence/scrapy-demo-cloudwatch-log).
