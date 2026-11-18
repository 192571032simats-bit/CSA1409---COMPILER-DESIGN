from ir import Emitter


class BooleanGenerator:
    def __init__(self, emitter=None):
        self.emitter = emitter or Emitter()

    def compare(self, left, op, right):
        truelist = self.emitter.makelist(self.emitter.emit(f"if {left} {op} {right} goto _"))
        falselist = self.emitter.makelist(self.emitter.emit("goto _"))
        return truelist, falselist

    def boolean_and(self, left_true, left_false, right_true, right_false):
        marker = self.emitter.nextquad
        self.emitter.backpatch(left_true, marker)
        return self.emitter.merge(left_false, right_true), right_false

    def boolean_or(self, left_true, left_false, right_true, right_false):
        marker = self.emitter.nextquad
        self.emitter.backpatch(left_false, marker)
        return self.emitter.merge(left_true, right_true), right_false

    def boolean_not(self, true_list, false_list):
        return false_list, true_list

    def if_then(self, true_list, false_list, statement_list=None):
        true_target = self.emitter.nextquad
        self.emitter.backpatch(true_list, true_target)
        return false_list
