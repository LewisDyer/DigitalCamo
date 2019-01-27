# DigitalCamo

DigitalCamo is a program that non-deterministically generates a pattern that, in some sense, looks like "digital camouflage". DigitalCamo also has support for defining your own custom colour palettes, along with image masks.

![Sample output of an early version of DigitalCamo](https://user-images.githubusercontent.com/33163858/51806367-19bd5c80-2271-11e9-8473-bbc18a50aaeb.png)
> Here's an indication of the sort of patterns the program generates. Subject to change!

---
I originally started working on this project after starting to learn about _generative art_ - the technique of generating art, in part or in whole, using some sort of autonomous system. 

Bear with me for the time being - this repo is very much a work in progress. More detailed documentation will be added in due time (I hope!)

## Upcoming Changes and Features

Here's a list of changes and features I'm hoping to include in the near future, broadly speaking from earliest to latest:

* Improve performance by checking if a mask already exists before recreating it

* Implement support for transparency, making the outputted images more suitable for the likes of creating icons

* Refactor the code into separate files for improved maintainability, including improved commenting

* Improve the usability of the program with a command line interface

* Allow for inverted image masks (filling in lighter sections of an image rather than darker sections)

* Allow for combining two palettes into one image using inverted image masks


