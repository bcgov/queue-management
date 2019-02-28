#!/usr/bin/env bash

# Borrowed from https://github.com/mendersoftware/integration/blob/master/keygen
# generate keys for signing JSON Web Tokens
ROOTDIR=$(pwd)/keys-generated
KEYDIR=$ROOTDIR/keys
FILE_NAME_PRIVATE_KEY="private.key"

mkdir -p "$KEYDIR"
cd "$KEYDIR"

for DIR in deviceauth useradm
do
  mkdir $DIR
  (
    cd $DIR
    openssl genpkey -algorithm RSA -out $FILE_NAME_PRIVATE_KEY -pkeyopt rsa_keygen_bits:3072

    # convert to RSA private key format, otherwise services complain:"
    # level=fatal msg="failed to read rsa private key: jwt: can't open key - not an rsa private key" file=proc.go func=runtime.main line=183
    openssl rsa -in $FILE_NAME_PRIVATE_KEY -out $FILE_NAME_PRIVATE_KEY
  )
done
