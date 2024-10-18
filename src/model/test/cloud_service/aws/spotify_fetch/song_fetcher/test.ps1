sam local invoke "PortamentoSongFetcher" --event mock_sf_event1.json -t $TEMPLATE_PATH
sam local invoke "PortamentoSongFetcher" --event mock_sf_event2.json -t $TEMPLATE_PATH
sam local invoke "PortamentoSongFetcher" --event mock_sf_event3.json -t $TEMPLATE_PATH
sam local invoke "PortamentoSongFetcher" --event mock_sf_event4.json -t $TEMPLATE_PATH