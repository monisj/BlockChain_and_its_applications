#!/bin/bash

LAST_TX_ID=""

while true; do
    TXS=$(multichain-cli mychain listwallettransactions | jq -c '.[]')
    
    for TX in $TXS; do
        TXID=$(echo $TX | jq -r '.txid')
        if [[ "$TXID" != "$LAST_TX_ID" ]]; then
            SENDER=$(echo $TX | jq -r '.details[0].address')
            RECEIVER=$(echo $TX | jq -r '.details[1].address')
            AMOUNT=$(echo $TX | jq -r '.details[1].amount')
            TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

            multichain-cli mychain publish global_ledger "$TXID" \
              "{\"json\":{\"sender\":\"$SENDER\",\"receiver\":\"$RECEIVER\",\"amount\":$AMOUNT,\"timestamp\":\"$TIME\"}}"

            LAST_TX_ID=$TXID
        fi
    done
    sleep 5
done
