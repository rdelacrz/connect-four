# connect-four
Contains logic to not only implement Connect Four, but create an AI that uses various algorithms to play the game optimally.

## Implementation
The UI interface is implemented using Vue with Typescript, and is linked to the Python-based backend logic via CEF Python, which hosts the UI in its own self-hosted application window frame.

## Motivation
One of the purposes of this project was to familiarize myself with Vue 3, which is the Javascript framework I am least acquianted with amongst the three major Javascript frameworks of today (Angular, React, and Vue). I also wanted to find an Pythonic alternative to Electron to utilize HTML and CSS's powerful UI capabilities while still being able to use Python for the backend data logic.

But most importantly, I wanted to teach myself how to develop my own AI using established algorithms such as Minimax and Alpha-Beta pruning. I ultimately hope to be able to use deep learning to create a self-learning AI and see if it is able to compete with other more standard AI algorithms.