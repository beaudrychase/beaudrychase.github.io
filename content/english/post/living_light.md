---
title: "Living_light"
date: 2023-03-24T15:15:38-05:00
Description: "This is my first post about my ongoing personal project living_light. In this post I will introduce the project and describe my intentions for creating it."
Tags: ["embedded"]
Categories: ["Dev"]
DisableComments: false
Draft: false
image: "/images/living_light_front.jpeg"
---

This is my first post about my ongoing personal project, living_light. In this post I introduce the project and describe my intentions for creating it.

## What is living_light

living_light is a decorative lamp that slowly rises and falls in brightness at the rate of meditative breathing. The color and brightness follow the day's natural progression and our circadian rhythms. During the day, it is a bright blueish-white and then at sunset, it transitions to a dark red for the night.
This lighting cycle follows research on the impact exposure to different colored light has on our ability to sleep at night.
Exposure to blue and white light during the day helps you fall asleep at night, while exposure to them at night can make it hard to sleep ([source](https://pubmed.ncbi.nlm.nih.gov/25535358/)). Red light, on the other hand, has little effect on our circadian rhythms, so exposure at night minimally impacts sleep ([source](https://pubmed.ncbi.nlm.nih.gov/30311830/)).
The light serves as an open invitation to pause to take a breath and a reminder to tap into nature and follow our biological rythm and the Earth's solar cycle.

![picture](/images/living_light_back.jpeg "The prototype is a Adafruit Huzzah32 mounted on a breadboard and connected to a 8x8 LED matrix that lives in a ziplock bag to keep everything together. I aim to make a more respectable 3d printed housing in the future.")

Currently the light intentionally has a very limited user interface. I had spent a lot of time implementing a text interface to change the behavior of the light through Telegram messenger's bot API that would take simple commands to change the length of the breath cycle, the color, and brightness.
However, I found that having these options changed the way I engaged with the light; I found myself distracted by assessing whether or not I should change the settings instead of meditating with it. Having these options detracted from the experience I designed, so I removed them. The interface is now intentionally restrained, the only way to interact with it is to look at it.

## My Development Journey

I began working on this project Summer of 2020. I had just finished the first semester of online classes after the pandemic upended in person activities. I had my first internship that summer, while the world was still transitioning to work from home.
Suddenly my world was circumscribed to my childhood bedroom and my internet connection. Between navigating online work, social isolation, and doomscrolling, my mental health declined.

This project is my reaction against that time of my life. At a time when everything I did was online, I wanted to work on something I could hold, see, and feel. When I felt distracted, anxious, and not present I wanted to build something to help me feel grounded in the present.
I wanted a reminder that even though everything else was interrupted, the cycle of the day continues. Thus the project began to take shape.

![picture](/images/living_light_early_prototype.jpeg "An early prototype running on an Arduino Uno.")

I've been incrementally and intermittantly working on the project ever since. It has been a fun project to work with and I'm happy that it has pushed me to learn.

I hope you have a better understanding of my light project. Check back in for future posts where I delve into the technical aspects of living_light!
