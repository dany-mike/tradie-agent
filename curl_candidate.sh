#!/usr/bin/env bash
# POST /launch/ - expects CandidateProfile body (see InputBody.json)

curl -X POST "http://127.0.0.1:8000/launch/" \
  -H "Content-Type: application/json" \
  -d @InputBody.json
