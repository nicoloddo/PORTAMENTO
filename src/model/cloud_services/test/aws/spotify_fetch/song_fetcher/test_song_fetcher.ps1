sam local invoke "PortamentoSongFetcher" --event mock_sqs_event1.json -t ../template.yml
sam local invoke "PortamentoSongFetcher" --event mock_sqs_event2.json -t ../template.yml
sam local invoke "PortamentoSongFetcher" --event mock_sqs_event3.json -t ../template.yml
sam local invoke "PortamentoSongFetcher" --event mock_sqs_event4.json -t ../template.yml