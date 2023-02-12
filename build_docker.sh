#!/bin/bash

# Build the Docker image
docker build -t vvarimo/micronode .
docker push vvarimo/micronode:latest