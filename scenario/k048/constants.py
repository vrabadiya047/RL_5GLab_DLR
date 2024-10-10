#!/usr/bin/env python3

from scenario.tls_control_basics.phase import Phase, PhaseTransition
from scenario.k048.enum import SGR_K048

class K048_PhasesAndTransitions:
    def __init__(self) -> None:
        
        signals = [s for s in SGR_K048]

        self.phase_1     = Phase.getObjectFromString(signals, "ggrgrgrrgrgrrrrrgrrrrggg")
        self.phase_2     = Phase.getObjectFromString(signals, "rgrrgrrrrrgrrgrrgrrrrrrr")
        self.phase_3     = Phase.getObjectFromString(signals, "rgrrrrrrrgrrggggrrrrrrrr")
        self.phase_4     = Phase.getObjectFromString(signals, "rggrrrrrrgrrrrrrrrrrrrrr")
        self.phase_5     = Phase.getObjectFromString(signals, "rrrrrgggrrrrrrrrrrgrrrrr")
        self.phase_6     = Phase.getObjectFromString(signals, "rrrrrgggrrrgrrrrrgrrgrrr")
        self.phase_fw1   = Phase.getObjectFromString(signals, "rgrgggrrrrrrrrrrrrrrrrrr")
        self.phase_fw2   = Phase.getObjectFromString(signals, "rgrrrgggrrrrrrrrrrrrrrrr")
        self.aus_um      = Phase.getObjectFromString(signals, "rrrrrrrrrrrrrrrrrrrrrrrr")

        # transition 1 -> 2, dur: 9

        trans_1_2_a = Phase.getObjectFromString(signals, "ygryrgrrgrgrrrrrgrrrrgrg") # 0
        trans_1_2_b = Phase.getObjectFromString(signals, "ygryrgrrgrgrrrrrgrrrrgrr") # 1
        trans_1_2_c = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrgrrrrgrr") # 3
        trans_1_2_d = Phase.getObjectFromString(signals, "rgrrrgrryrgrrrrrgrrrrgrr") # 4
        trans_1_2_e = Phase.getObjectFromString(signals, "rgrrryrryrgrrgrrgrrrrgrr") # 5
        trans_1_2_f = Phase.getObjectFromString(signals, "rgrrryrrrrgrrgrrgrrrrgrr") # 6
        trans_1_2_g = Phase.getObjectFromString(signals, "rgrrgrrrrrgrrgrrgrrrrgrr") # 7
        trans_1_2_h = Phase.getObjectFromString(signals, "rgrrgrrrrrgrrgrrgrrrrrrr") # 8

        self.trans_1_2 = PhaseTransition.getObject([
            (1, trans_1_2_a),
            (2, trans_1_2_b),
            (1, trans_1_2_c),
            (1, trans_1_2_d),
            (1, trans_1_2_e),
            (1, trans_1_2_f),
            (1, trans_1_2_g),
            (1, trans_1_2_h)
        ])

        # transition 1 -> 3, dur: 15

        trans_1_3_a = Phase.getObjectFromString(signals, "ygryrgrrgrgrrrrrgrrrrgrg") #  0
        trans_1_3_b = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrgrrrrgrg") #  3
        trans_1_3_c = Phase.getObjectFromString(signals, "rgrrryrrgrgrrgrrrrrrrgrr") #  5
        trans_1_3_d = Phase.getObjectFromString(signals, "rgrrryrryrgrrgrrrrrrrgrr") #  6
        trans_1_3_e = Phase.getObjectFromString(signals, "rgrrryrrrrgrrgrrrrrrrgrr") #  8
        trans_1_3_f = Phase.getObjectFromString(signals, "rgrrrrrrrugrrgrrrrrrrgrr") #  9
        trans_1_3_g = Phase.getObjectFromString(signals, "rgrrrrrrrggrggggrrrrrgrr") # 10

        self.trans_1_3 = PhaseTransition.getObject([
            (3, trans_1_3_a),
            (2, trans_1_3_b),
            (1, trans_1_3_c),
            (2, trans_1_3_d),
            (1, trans_1_3_e),
            (1, trans_1_3_f),
            (2, trans_1_3_g),
        ])

        # transition 1 -> 5, dur: 16

        trans_1_5_a = Phase.getObjectFromString(signals, "ygryrgrrgrgrrrrrrrrrrgrr") #  0
        trans_1_5_b = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrrrrrrgrr") #  3
        trans_1_5_c = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrrrrrrrrr") #  4
        trans_1_5_d = Phase.getObjectFromString(signals, "rgrrrgrryrgrrrrrrrrrrrrr") #  5
        trans_1_5_e = Phase.getObjectFromString(signals, "ryrrrgrrrryrrrrrrrrrrrrr") #  7
        trans_1_5_f = Phase.getObjectFromString(signals, "ryrrrgrrrrrrrrrrrrrrrrrr") #  9
        trans_1_5_g = Phase.getObjectFromString(signals, "rrrrrgurrrrrrrrrrrgrrrrr") # 10
        trans_1_5_h = Phase.getObjectFromString(signals, "rrrrrggrrrrrrrrrrrgrrrrr") # 11
        trans_1_5_i = Phase.getObjectFromString(signals, "rrrrrggurrrrrrrrrrgrrrrr") # 13
        trans_1_5_j = Phase.getObjectFromString(signals, "rrrrrgggrrrrrrrrrrgrrrrr") # 14

        self.trans_1_5 = PhaseTransition.getObject([
            (3, trans_1_5_a),
            (1, trans_1_5_b),
            (1, trans_1_5_c),
            (2, trans_1_5_d),
            (2, trans_1_5_e),
            (1, trans_1_5_f),
            (1, trans_1_5_g),
            (2, trans_1_5_h),
            (1, trans_1_5_i),
            (2, trans_1_5_j),
        ])

        # transition 1 -> fw1, dur: 12
        trans_1_fw1_a = Phase.getObjectFromString(signals, "ygrgrgrryryrrrrrrrrrrgrg") # 0
        trans_1_fw1_b = Phase.getObjectFromString(signals, "ygrgrgrryryrrrrrrrrrrgrr") # 1
        trans_1_fw1_c = Phase.getObjectFromString(signals, "ygrgrgrrrrrrrrrrrrrrrgrr") # 2
        trans_1_fw1_d = Phase.getObjectFromString(signals, "rgrgrgrrrrrrrrrrrrrrrgrr") # 3
        trans_1_fw1_e = Phase.getObjectFromString(signals, "rgrgrgrrrrrrrrrrrrrrrgrr") # 6
        trans_1_fw1_f = Phase.getObjectFromString(signals, "rgrgggrrrrrrrrrrrrrrrgrr") # 7
        trans_1_fw1_g = Phase.getObjectFromString(signals, "rgrgggrrrrrrrrrrrrrrrrrr") # 8
        trans_1_fw1_h = Phase.getObjectFromString(signals, "rgrgggrrrrrrrrrrrrrrrrrr") # 9

        self.trans_1_fw1 = PhaseTransition.getObject([
            (1, trans_1_fw1_a),
            (1, trans_1_fw1_b),
            (1, trans_1_fw1_c),
            (3, trans_1_fw1_d),
            (1, trans_1_fw1_e),
            (1, trans_1_fw1_f),
            (1, trans_1_fw1_g),
            (3, trans_1_fw1_h)
        ])

        # transition 1 -> fw2, dur: 21

        trans_1_fw2_a = Phase.getObjectFromString(signals, "ygryrgrryryrrrrrrrrrrgrr") # 0
        trans_1_fw2_b = Phase.getObjectFromString(signals, "ygryrgrrrrrrrrrrrrrrrgrr") # 2
        trans_1_fw2_c = Phase.getObjectFromString(signals, "rgrrrgrrrrrrrrrrrrrrrgrr") # 3
        trans_1_fw2_d = Phase.getObjectFromString(signals, "rgrrrgrrrrrrrrrrrrrrrrrr") # 8
        trans_1_fw2_e = Phase.getObjectFromString(signals, "rgrrrguurrrrrrrrrrrrrrrr") # 15
        trans_1_fw2_f = Phase.getObjectFromString(signals, "rgrrrgggrrrrrrrrrrrrrrrr") # 16

        self.trans_1_fw2 = PhaseTransition.getObject([
            (2, trans_1_fw2_a),
            (1, trans_1_fw2_b),
            (5, trans_1_fw2_c),
            (7, trans_1_fw2_d),
            (1, trans_1_fw2_e),
            (5, trans_1_fw2_f)
        ])

        # transition 2 -> 3, dur: 6

        trans_2_3_a = Phase.getObjectFromString(signals, "rgrrgrrrrugrrgrrrrrrrrrr") # 0
        trans_2_3_a = Phase.getObjectFromString(signals, "rgrrgrrrrggrggggrrrrrrrr") # 1
        trans_2_3_a = Phase.getObjectFromString(signals, "rgrrgrrrrgyrggggrrrrrrrr") # 2
        trans_2_3_a = Phase.getObjectFromString(signals, "rgrrgrrrrgrrggggrrrrrrrr") # 4

        self.trans_2_3 = PhaseTransition.getObject([
            (1, trans_2_3_a),
            (1, trans_2_3_a),
            (2, trans_2_3_a),
            (2, trans_2_3_a)
        ])

        # trans 2 -> 5, dur: 15

        trans_2_5a = Phase.getObjectFromString(signals, "rgrrgrrrrugrrgrrgrrrrrrr") # 0
        trans_2_5b = Phase.getObjectFromString(signals, "rgrrgrrrrggrgrgggrrrrrrr") # 1
        trans_2_5c = Phase.getObjectFromString(signals, "rgrrrrrrrggrgrgggrrrrrrr") # 4
        trans_2_5d = Phase.getObjectFromString(signals, "rgrrrrrrrgyrgrrrrrrrrrrr") # 6
        trans_2_5e = Phase.getObjectFromString(signals, "ryrrrrrrrgrrgrrrrrgrrrrr") # 8
        trans_2_5f = Phase.getObjectFromString(signals, "ryrrrrurryrrgrrrrrgrrrrr") # 9
        trans_2_5g = Phase.getObjectFromString(signals, "ryrrrrgrryrrgrrrrrgrrrrr") # 10
        trans_2_5h = Phase.getObjectFromString(signals, "rrrrrrgrrrrrgrrrrrgrrrrr") # 11
        trans_2_5i = Phase.getObjectFromString(signals, "rrrrrugurrrrgrrrrrgrrrrr") # 12
        trans_2_5j = Phase.getObjectFromString(signals, "rrrrrgggrrrrgrrrrrgrrrrr") # 13

        self.trans_2_5 = PhaseTransition.getObject([
            (1, trans_2_5a),
            (3, trans_2_5b),
            (2, trans_2_5c),
            (2, trans_2_5d),
            (1, trans_2_5e),
            (1, trans_2_5f),
            (1, trans_2_5g),
            (1, trans_2_5h),
            (1, trans_2_5i),
            (2, trans_2_5j),
        ])


        # transition 3 -> 4,, dur: 10

        trans_3_4_a = Phase.getObjectFromString(signals, "rgrrrrrrrgrrgrggrrrrrrrr") # 0
        trans_3_4_b = Phase.getObjectFromString(signals, "rgurrrrrrgrrgrgrrrrrrrrr") # 4
        trans_3_4_c = Phase.getObjectFromString(signals, "rggrrrrrrgrrgrgrrrrrrrrr") # 5

        self.trans_3_4 = PhaseTransition.getObject([
            (4, trans_3_4_a),
            (1, trans_3_4_b),
            (1, trans_3_4_c)
        ])

        # transition 4 -> 1, dur: 22

        trans_4_1_a = Phase.getObjectFromString(signals, "rgyrrrrrryrrrrrrrrrrrrrr") # 0
        trans_4_1_b = Phase.getObjectFromString(signals, "rgyrrrrrrrrrrrrrrrrrrrrr") # 2
        trans_4_1_c = Phase.getObjectFromString(signals, "rgrrrrrrrrrrrrrrrrrrrrrr") # 3
        trans_4_1_d = Phase.getObjectFromString(signals, "rgrrrurrrrrrrrrrrrrrrrrr") # 6
        trans_4_1_e = Phase.getObjectFromString(signals, "rgrrrgrrrrrrrrrrrrrrrrrr") # 7
        trans_4_1_f = Phase.getObjectFromString(signals, "rgrrrgrrururrrrrrrrrrrrr") # 14
        trans_4_1_g = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrgrrrrggg") # 15
        trans_4_1_h = Phase.getObjectFromString(signals, "ugrurgrrgrgrrrrrgrrrrggg") # 16
        trans_4_1_i = Phase.getObjectFromString(signals, "ggrgrgrrgrgrrrrrgrrrrggg") # 17

        self.trans_4_1 = PhaseTransition.getObject([
            (2, trans_4_1_a),
            (1, trans_4_1_b),
            (3, trans_4_1_c),
            (1, trans_4_1_d),
            (7, trans_4_1_e),
            (1, trans_4_1_f),
            (1, trans_4_1_g),
            (1, trans_4_1_h),
            (5, trans_4_1_i),
        ])

        # transition 4 -> 5, dur: 10

        trans_4_5_a = Phase.getObjectFromString(signals, "rgyrrrrrrgrrrrrrrrrrrrrr") # 0
        trans_4_5_b = Phase.getObjectFromString(signals, "rgrrrrrrrgrrrrrrrrrrrrrr") # 3
        trans_4_5_c = Phase.getObjectFromString(signals, "rgrrrrrrryrrrrrrrrgrrrrr") # 4
        trans_4_5_d = Phase.getObjectFromString(signals, "rgrrrrurryrrrrrrrrgrrrrr") # 5
        trans_4_5_e = Phase.getObjectFromString(signals, "ryrrrrgrrrrrrrrrrrgrrrrr") # 6
        trans_4_5_f = Phase.getObjectFromString(signals, "ryrrrugrrrrrrrrrrrgrrrrr") # 7
        trans_4_5_g = Phase.getObjectFromString(signals, "ryrrrggrrrrrrrrrrrgrrrrr") # 8
        trans_4_5_h = Phase.getObjectFromString(signals, "rrrrrggrrrrrrrrrrrgrrrrr") # 9

        self.trans_4_5 = PhaseTransition.getObject([
            (3, trans_4_5_a),
            (1, trans_4_5_b),
            (1, trans_4_5_c),
            (1, trans_4_5_d),
            (1, trans_4_5_e),
            (1, trans_4_5_f),
            (1, trans_4_5_g),
            (1, trans_4_5_h),
        ])

        # transition 4 -> fw1, dur 17

        trans_4_fw1_a = Phase.getObjectFromString(signals, "rgyrrrrrryrrrrrrrrrrrrrr") # 0
        trans_4_fw1_b = Phase.getObjectFromString(signals, "rgyrrrrrrrrrrrrrrrrrrrrr") # 2
        trans_4_fw1_c = Phase.getObjectFromString(signals, "rgrrrrrrrrrrrrrrrrrrrrrr") # 3
        trans_4_fw1_d = Phase.getObjectFromString(signals, "rgrururrrrrrrrrrrrrrrrrr") # 11
        trans_4_fw1_e = Phase.getObjectFromString(signals, "rgrgggrrrrrrrrrrrrrrrrrr") # 12

        self.trans_4_fw1 = PhaseTransition.getObject([
            (2, trans_4_fw1_a),
            (1, trans_4_fw1_b),
            (8, trans_4_fw1_c),
            (1, trans_4_fw1_d),
            (5, trans_4_fw1_e)
        ])

        # transition 4 -> fw2, dur: 16

        trans_4_fw2_a = Phase.getObjectFromString(signals, "rgyrrrrrryrrrrrrrrrrrrrr") # 0
        trans_4_fw2_b = Phase.getObjectFromString(signals, "rgyrrrrrrrrrrrrrrrrrrrrr") # 2
        trans_4_fw2_c = Phase.getObjectFromString(signals, "rgrrrrrrrrrrrrrrrrrrrrrr") # 3
        trans_4_fw2_d = Phase.getObjectFromString(signals, "rgrrruuurrrrrrrrrrrrrrrr") # 10
        trans_4_fw2_e = Phase.getObjectFromString(signals, "rgrrrgggrrrrrrrrrrrrrrrr") # 11

        self.trans_4_fw2 = PhaseTransition.getObject([
            (2, trans_4_fw2_a),
            (1, trans_4_fw2_b),
            (7, trans_4_fw2_c),
            (1, trans_4_fw2_d),
            (5, trans_4_fw2_e)
        ])

        # transition 5 -> 6, dur: 9

        trans_5_6_a = Phase.getObjectFromString(signals, "rrrrrgggrrrurrrrrrrrrrrr") # 0
        trans_5_6_b = Phase.getObjectFromString(signals, "rrrrrgggrrrgrrrrrgrggrrr") # 1
        trans_5_6_c = Phase.getObjectFromString(signals, "rrrrrgggrrrgrrrrrgrrgrrr") # 7

        self.trans_5_6 = PhaseTransition.getObject([
            (1, trans_5_6_a),
            (6, trans_5_6_b),
            (2, trans_5_6_c)
        ])

        # transition 6 -> 1, dur: 24

        trans_6_1_a = Phase.getObjectFromString(signals, "rrrrrgyyrrrgrrrrrgrrrrrr") # 0
        trans_6_1_b = Phase.getObjectFromString(signals, "rrrrrgrrrrryrrrrrgrrrrrr") # 3
        trans_6_1_c = Phase.getObjectFromString(signals, "rrrrrgrrurryrrrrrgrrrrrr") # 4
        trans_6_1_d = Phase.getObjectFromString(signals, "rrrrrgrrgrrrrrrrrrrrrggg") # 5
        trans_6_1_e = Phase.getObjectFromString(signals, "rurrrgrrgrrrrrrrrrrrrggg") # 6
        trans_6_1_f = Phase.getObjectFromString(signals, "rgrrrgrrgrrrrrrrrrrrrggg") # 7
        trans_6_1_g = Phase.getObjectFromString(signals, "rgrrrgrrgrurrrrrrrrrrggg") # 10
        trans_6_1_h = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrrrrrrggg") # 11
        trans_6_1_i = Phase.getObjectFromString(signals, "ugrurgrrgrgrrrrrrrrrrggg") # 13
        trans_6_1_j = Phase.getObjectFromString(signals, "ggrgrgrrgrgrrrrrgrrrrggg") # 14

        self.trans_6_1 = PhaseTransition.getObject([
            (3, trans_6_1_a),
            (1, trans_6_1_b),
            (1, trans_6_1_c),
            (1, trans_6_1_d),
            (1, trans_6_1_e),
            (3, trans_6_1_f),
            (1, trans_6_1_g),
            (2, trans_6_1_h),
            (1, trans_6_1_i),
            (10, trans_6_1_j)
        ])

        # transition 6 -> fw1, dur: 19

        trans_6_fw1_a = Phase.getObjectFromString(signals, "rrrrrgyyrrryrrrrrgrrrrrr") # 0
        trans_6_fw1_b = Phase.getObjectFromString(signals, "rrrrrgyyrrrrrrrrrgrrrrrr") # 2
        trans_6_fw1_c = Phase.getObjectFromString(signals, "rrrrrgrrrrrrrrrrrgrrrrrr") # 3
        trans_6_fw1_d = Phase.getObjectFromString(signals, "rrrrrgrrrrrrrrrrrrrrrrrr") # 5
        trans_6_fw1_e = Phase.getObjectFromString(signals, "rururgrrrrrrrrrrrrrrrrrr") # 13
        trans_6_fw1_f = Phase.getObjectFromString(signals, "rgrgggrrrrrrrrrrrrrrrrrr") # 14

        self.trans_6_fw1 = PhaseTransition.getObject([
            (2, trans_6_fw1_a),
            (1, trans_6_fw1_b),
            (2, trans_6_fw1_c),
            (8, trans_6_fw1_d),
            (1, trans_6_fw1_e),
            (5, trans_6_fw1_f)
        ])

        # transition 6 -> fw2, dur: 12

        trans_6_fw2_a = Phase.getObjectFromString(signals, "rrrrrgggrrryrrrrrgrrrrrr") # 0
        trans_6_fw2_b = Phase.getObjectFromString(signals, "rrrrrgggrrrrrrrrrgrrrrrr") # 2
        trans_6_fw2_c = Phase.getObjectFromString(signals, "rrrrrgggrrrrrrrrrrrrrrrr") # 5
        trans_6_fw2_d = Phase.getObjectFromString(signals, "rurrrgggrrrrrrrrrrrrrrrr") # 6
        trans_6_fw2_e = Phase.getObjectFromString(signals, "rgrrrgggrrrrrrrrrrrrrrrr") # 7

        self.trans_6_fw2 = PhaseTransition.getObject([
            (2, trans_6_fw2_a),
            (3, trans_6_fw2_b),
            (1, trans_6_fw2_c),
            (1, trans_6_fw2_d),
            (5, trans_6_fw2_e)
        ])

        # transition fw1 -> 1, dur: 14

        trans_fw1_1_a = Phase.getObjectFromString(signals, "rgryrgrrrrrrrrrrrrrrrrrr") # 0
        trans_fw1_1_b = Phase.getObjectFromString(signals, "rgrrrgrrrrrrrrrrrrrrrrrr") # 3
        trans_fw1_1_c = Phase.getObjectFromString(signals, "rgrrrgrrurrrrrrrrrrrrrrr") # 5
        trans_fw1_1_d = Phase.getObjectFromString(signals, "rgrrrgrrgrurrrrrrrrrrrrr") # 6
        trans_fw1_1_e = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrgrrrrggg") # 7
        trans_fw1_1_f = Phase.getObjectFromString(signals, "ugrurgrrgrgrrrrrgrrrrggg") # 8
        trans_fw1_1_g = Phase.getObjectFromString(signals, "ggrgrgrrgrgrrrrrgrrrrggg") # 9

        self.trans_fw1_1 = PhaseTransition.getObject([
            (3, trans_fw1_1_a),
            (2, trans_fw1_1_b),
            (1, trans_fw1_1_c),
            (1, trans_fw1_1_d),
            (1, trans_fw1_1_e),
            (1, trans_fw1_1_f),
            (5, trans_fw1_1_g)
        ])

        # transition fw2 -> 1, dur: 19

        trans_fw2_1_a = Phase.getObjectFromString(signals, "rgrrrgyyrrrrrrrrrrrrrrrr") # 0
        trans_fw2_1_b = Phase.getObjectFromString(signals, "rgrrrgrrrrrrrrrrrrrrrrrr") # 3
        trans_fw2_1_c = Phase.getObjectFromString(signals, "rgrrrgrrurrrrrrrrrrrrrrr") # 4
        trans_fw2_1_d = Phase.getObjectFromString(signals, "rgrrrgrrgrrrrrrrrrrrrrrr") # 5
        trans_fw2_1_e = Phase.getObjectFromString(signals, "rgrrrgrrgrurrrrrrrrrrrrr") # 10
        trans_fw2_1_f = Phase.getObjectFromString(signals, "rgrrrgrrgrgrrrrrrrrrrrrr") # 11
        trans_fw2_1_g = Phase.getObjectFromString(signals, "ugrurgrrgrgrrrrrrrrrrrrr") # 13
        trans_fw2_1_h = Phase.getObjectFromString(signals, "ggrgrgrrgrgrrrrrgrrrrggg") # 14

        self.trans_fw2_1 = PhaseTransition.getObject([
            (1, trans_fw2_1_a),
            (1, trans_fw2_1_b),
            (1, trans_fw2_1_c),
            (1, trans_fw2_1_d),
            (1, trans_fw2_1_e),
            (1, trans_fw2_1_f),
            (1, trans_fw2_1_g),
            (1, trans_fw2_1_h)
        ])