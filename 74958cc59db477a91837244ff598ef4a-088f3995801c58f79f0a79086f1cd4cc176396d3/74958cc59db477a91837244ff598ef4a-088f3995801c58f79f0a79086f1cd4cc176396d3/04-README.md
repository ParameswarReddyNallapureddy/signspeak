### We have to add the HandGestureRecognitionCalculator node config in the in the hand_landmark_cpu.pbtxt or hand_landmark_gpu.pbtxt graph file.

```js  
  node {
      calculator: "HandGestureRecognitionCalculator"
      input_stream: "NORM_LANDMARKS:scaled_landmarks"
      input_stream: "NORM_RECT:hand_rect_for_next_frame"
    }
```

For example:
1. in the **hand_landmark_cpu.pbtx** see here: https://github.com/TheJLifeX/mediapipe/blob/master/mediapipe/graphs/hand_tracking/subgraphs/hand_landmark_cpu.pbtxt#L187-L191
2. in the **hand_landmark_gpu.pbtx** see here: https://github.com/TheJLifeX/mediapipe/blob/master/mediapipe/graphs/hand_tracking/subgraphs/hand_landmark_gpu.pbtxt#L182-L186