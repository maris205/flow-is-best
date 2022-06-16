#!/bin/sh
nft_name="Wow" #NFT名称
find ./ -name "*.cdc"|xargs -i sed 's/Example/'''${nft_name}'''/g' {}