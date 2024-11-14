# Next Word Prediction
Next Word Prediction using Language Models.

Three Language Models have been used:
1. Trigram Language Model with Backoff
2. LSTM Language Model

They have been trained on "Time Machine" by H.G. Wells. The text is saved as "time_machine.txt".

## Results
Initial context: `this is`  
Number of generated words: 20

1. Trigram LM with Backoff
```
this is so extensively overlooked continued the time traveller was not too strongly for even a library to me i don t
```

2. LSTM LM (trained for 10 epochs)
```
this is more than a gallery of simply colossal proportions but singularly ill lit the floor of
```
