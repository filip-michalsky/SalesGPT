#!/bin/bash
export $(grep -v '^#' ../.env | xargs)
nodemon --watch pages --watch components --exec "next dev"
