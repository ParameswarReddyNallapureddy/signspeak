# Simple Hand Gesture Recognition Code - Hand tracking - Mediapipe
Goal of this gist is to recognize **ONE**, **TWO**, **TREE**, **FOUR**, **FIVE**, **SIX**, **YEAH**, **ROCK**, **SPIDERMAN** and **OK**.
We use the **LANDMARKS** output of the *LandmarkLetterboxRemovalCalculator*. This output is a landmark list that contains 21 landmark. 
In the ***[02-landmarks.jpg](#file-02-landmarks-jpg)*** picture below you can see the index of each landmark. 
Each landmark have  **x**, **y** and **z** values. But only **x**, **y** values are sufficient for our Goal.
If you dont want to copy/paste each the code on this gist, you can clone my forked version of mediapipe here: https://github.com/TheJLifeX/mediapipe. 
I have already commited all code in that repository.

We have five finger states.
 1. thumbIsOpen  
 2. firstFingerIsOpen  
 3. secondFingerIsOpen 
 4. thirdFingerIsOpen  
 5. fourthFingerIsOpen
 
 For exmaple: thumb is **open** if the x value of landmark 3 and the x value of landmark 4 are less than x value of landmark 2 else it is **close**
 
 PS: thumb open/close works only for the right hand. 
 Because we can not yet determine if you show your left or right hand. For more info see this issue: [Can `palm_detection` distinguish between right and left hand?](https://github.com/google/mediapipe/issues/127)
 
**Prerequisite**:
You kwon how to run the *hand tracking* example.
1. [Get Started with mediapipe](https://google.github.io/mediapipe/getting_started/getting_started.html)
2. [Hand Tracking on Desktop](https://google.github.io/mediapipe/solutions/hands.html#desktop)

If you want to know how to recognize some simple hand mouvements like **Scrolling**, **Zoom in/out** and **Slide left/right** (see [comment](https://gist.github.com/TheJLifeX/74958cc59db477a91837244ff598ef4a#gistcomment-3299798) below) you can read this gist: [Simple Hand Mouvement Recognition Code](https://gist.github.com/TheJLifeX/99cdf4823e2b7867c0e94fabc660c58b).