### We have to add the path to the "hand-gesture-recognition-calculator" bazel build config in the hand_landmark_cpu or hand_landmark_cpu bazel build config.

For example: *"//hand-gesture-recognition:hand-gesture-recognition-calculator"*
1. in the **hand_landmark_cpu** see here: https://github.com/TheJLifeX/mediapipe/blob/a069e5b6e1097f3f69c161a11f336e9e3b9751dd/mediapipe/graphs/hand_tracking/subgraphs/BUILD#L88 
2. in the **hand_landmark_gpu** see here: https://github.com/TheJLifeX/mediapipe/blob/a069e5b6e1097f3f69c161a11f336e9e3b9751dd/mediapipe/graphs/hand_tracking/subgraphs/BUILD#L192