# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'


class PickModel():
    num_pick_models = 0

    def __init__(self, number_picks):
        self.id = PickModel.num_pick_models
        PickModel.num_pick_models += 1

        self._prefix = "id"+str(self.id)+"_"

        self.current_pick = 0
        self.number_picks = number_picks
        self.pick_points = [Point()] * number_picks
        self._parse_params()
        self.parameters = self.make_params()

    def update_current_parameter(self, x, y):
        raise NotImplementedError

    def _parse_params(self):
        raise NotImplementedError

    def pick_parameter(self, x, y):
        self.update_current_parameter(x, y)
        self.pick_points[self.current_pick].x = x
        self.pick_points[self.current_pick].y = y

        self.current_pick += 1
        if self.current_pick < self.number_picks:
            return True
        else:
            self.current_pick = 0
            return False

    def get_param(self, param_name):
        return self.parameters[param_name]

    def set_parameter_value(self, param_name, value):
        self.parameters["{}{}".format(self._prefix, param_name)].value = value

    def get_parameter_value(self, param_name):
        return self.parameters["{}{}".format(self._prefix, param_name)].value

    def set_parameter_max_value(self, param_name, max_value):
        self.parameters["{}{}".format(self._prefix, param_name)].max = max_value

    def get_parameter_max_value(self, param_name):
        return self.parameters["{}{}".format(self._prefix, param_name)].max

    def set_parameter_min_value(self, param_name, min_value):
        self.parameters["{}{}".format(self._prefix, param_name)].min = min_value

    def get_parameter_min_value(self, param_name):
        return self.parameters["{}{}".format(self._prefix, param_name)].min

    def quick_eval(self, x):
        return self.eval(self.parameters, x=x)

    def eval(self, *args, **kwargs):
        raise NotImplementedError

    def make_params(self, *args, **kwargs):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls()

        for parameter_name in self._param_root_names:
            # print result.parameters
            # print self.parameters
            result_param = result.get_param("{}{}".format(result._prefix, parameter_name))
            current_param = self.get_param("{}{}".format(self._prefix, parameter_name))

            result_param.value = current_param.value
            result_param.vary   = current_param.vary
            result_param.min = current_param.min
            result_param.max = current_param.max

        return result


class Point():
    def __init__(self, x=0., y=0.):
        self.x = x
        self.y = y