# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, get_time

def space_down(e):
    return e[0] == 'INPUT' and e[1] == 'SPACE_DOWN'

def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(boy):
        boy.action = 3
        boy.frame = 0
        boy.wait_time = get_time()
        pass
        # print('Idle Enter')

    @staticmethod
    def exit(boy):
        pass
        # print('Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 2:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        # print('Idle Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        # pass


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Sleep
        self.transitions = {
            Sleep: {space_down: Idle},
            Idle: {time_out: Sleep}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.boy)

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


class Sleep:
    @staticmethod
    def enter(boy):
        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                      3.141592 / 2, '', boy.x - 25, boy.y - 25,
                                      100, 100)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
