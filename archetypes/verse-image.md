---
title: {{ getenv "HUGO_POST_TITLE" }}  # "{{ replace .Name "-" " " | title }}"
type: verse_image
date: {{ .Date }}
image:  {{ getenv "HUGO_POST_IMG" }}
prompt:
tags:
    -
generators:
---
