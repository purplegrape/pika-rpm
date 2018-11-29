#!/usr/bin/env bash

set -e

CPU_NUM=$(grep -c processor /proc/cpuinfo)

mkdir -p /tmp/pika_deps

## build rocksdb
pushd third/rocksdb
  if [ ! -f /tmp/pika_deps/librocksdb.a ];then
    cmake3 \
    -DWITH_JEMALLOC:BOOL=ON \
    -DWITH_SNAPPY:BOOL=ON \
    -DWITH_ZLIB:BOOL=ON \
    -DWITH_BZ2:BOOL=ON \
    -DROCKSDB_LITE:BOOL=ON \
    -DPORTABLE:BOOL=ON .
  make -j $CPU_NUM
  install -D -p -m 644 librocksdb.a /tmp/pika_deps/librocksdb.a
  fi
popd

## build gperftools

## build libunwind

## build gflags

## build snappy

## build slash
