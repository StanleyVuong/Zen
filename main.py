+# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    debug_text = ''

    def print_debug(self):
        white = self.renderer.white()
        self.renderer.draw_string_2d(10, 150, 3, 3, self.debug_text, white)

    def run(self):
        self.print_debug()
        white = self.renderer.white()
        self.renderer.draw_line_3d(self.me.location, self.ball.location, white)

        if self.get_intent() is not None:
            self.debug_intent()
            return
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        is_in_front_of_ball = d1 > d2
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
    #     # if we're in front of the ball, retreat
        if is_in_front_of_ball:
            self.set_intent(goto(self.friend_goal.location))
            self.debug_text = 'retreating'
            return
        # self.set_intent(atba())

        near_the_ball = len(self(self.ball.location)) < len(
            self(self.freind_goal.location))
        if near_the_ball:
            self.set_intent(short_shot(self.foe_goal.location))
            return

        targets = {
            'at_opponent_goal': (self.foe.goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self, targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            print('at thier goal')
            return
        if len(hits['away_from_our_net']) > 0:
            print('away from our goal')
            self.set_intent(hits['away_from_our_net'][0])
            return

        if self.is_in_front_of_ball():
            self.set_intent(goto(self.friend_goal.location))
            return

        available_boost = [
            boost for boost in self.boost if boost.large and boost.active]
        if len(available_boost) > 0:
            self.set_intent(goto(available_boost[0].location))
            print('going for boost', available_boost[0].index)
            return

        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            self.debug_text = 'shooting'
            return

        closest_boost = self.get_closest_large_boost()
        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            self.debug_text = 'getting boost'
            return

        # if self.me.boost < 10:
        #     self.set_intent(closest_boost)
        #     return

        if self.location.x < (-892.755 + 100):
            self.set_intent(goto(ball_object))
            return

        available_boost = [
            boost for boost in self.boost if boost.large and boost.active]
        if len(available_boost) > 0:
            self.set_intent(goto(available_boost[0].location))
            print('going for boost', available_boost[0].index)
            return

        # if self.time % 2 == 0:
        #     print(hits)

        # set_intent tells the bot what it's trying to do
        # speed = 500
        # self.set_intent(drive(speed))

        # self.set_intent(jumper())
        # print(f'my x position is: {self.me.location.x} ')
