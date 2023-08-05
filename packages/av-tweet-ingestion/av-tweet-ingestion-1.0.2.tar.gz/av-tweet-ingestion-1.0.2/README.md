
# av-tweet-ingestion
  

Ingestion of tweets using Twitter's RecentAPI and upload to S3.

  
  

## Installation

  
  

```sh

pip install av-tweet-ingestion

```

  

## Usage example

  
<br>

### Setup Environmental Variables

  

BEARER_TOKEN="<twitter_bearer_token>"

  

S3_ACESS_KEY="<acess_key>"

S3_SECRET_KEY="<secret_key>"

  

S3_BUCKET_NAME="<bucket_name>"

S3_LANDING_LAYER="<landing_zone>"

  
  
<br>

### Define Query

```

query_params = {

'query': 'from: elonmusk',

'user.fields':'id,location,name,public_metrics,created_at',

'tweet.fields': 'author_id',

# 'expansions':'geo.place_id,author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id.author_id',

'max_results':'10'

}

```

  

<br>

  

### Ingest

```

BatchIngestor(query_params, # Query

1, # Number of pages to ingest

RecentAPI, # Titter's API to call

'test/RecentAPI', # Set address to save data

S3Writer).ingest() # Writer to be used

```

  

## Contributing

  

1. Fork it (<https://github.com/andreveit/av-tweet-ingestion/fork>)

2. Create your feature branch (`git checkout -b feature/fooBar`)

3. Commit your changes (`git commit -am 'Add some fooBar'`)

4. Push to the branch (`git push origin feature/fooBar`)

5. Create a new Pull Request

  

<!-- Markdown link & img dfn's -->

[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square

[npm-url]: https://npmjs.org/package/datadog-metrics

[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square

[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square

[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics

[wiki]: https://github.com/yourname/yourproject/wiki