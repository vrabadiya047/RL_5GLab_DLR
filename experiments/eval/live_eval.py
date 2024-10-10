from typing import Tuple, List
import matplotlib.pyplot as plt


class EvalData:
    def __init__(self, y_label: str = 'data', x_label: str = 'timestep') -> None:
        self._timesteps = []
        self._data = []
        self._y_label = y_label
        self._x_label = x_label
        return None

    def append(self, t: float, date: float) -> None:
        self._timesteps.append(t)
        self._data.append(date)
        return None

    def get_all(self) -> Tuple[List[float], List[float]]:
        return self._timesteps, self._data

    def get_data(self) -> List[float]:
        return self._data

    def get_ylabel(self) -> str:
        return self._y_label

    def _plot_vline(self, vline_pos: float = None) -> None:
        if vline_pos != None:
            diff = 0.1 * (max(self._data) - min(self._data))
            plt.vlines(vline_pos, min(self._data) - diff, max(self._data) + diff, colors='r', linestyles='dotted')
        return None

    def _get_labels(self, y_label, x_label) -> Tuple[str, str]:
        if x_label == None:
            x_label = self._x_label
        if y_label == None:
            y_label = self._y_label
        return x_label, y_label

    def _plot(self, start: int = 0, end: int = None, y_label: str = None, x_label: str = None, vline_pos: float = None,
              do_show: bool = True, legend=None) -> None:
        x_label, y_label = self._get_labels(x_label, y_label)
        if end == None:
            end = len(self._data)
        if legend == None:
            legend = [y_label]
        else:
            legend += [y_label]
        if vline_pos:
            legend += ['ev ins']
        plt.plot(self._timesteps[start:end], self._data[start:end])
        self._plot_vline(vline_pos)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if do_show:
            plt.legend(legend)
            plt.show()
        return None

    def plot(self, y_label: str = None, x_label: str = None, vline_pos: float = None, do_show: bool = True,
             legend=None) -> None:
        self._plot(y_label=y_label, x_label=x_label, vline_pos=vline_pos, do_show=do_show, legend=legend)
        return None

    def plot_clipped(self, start: int = 0, end: int = None, y_label: str = None, x_label: str = None,
                     vline_pos: float = None, do_show: bool = True, legend=None) -> None:
        self._plot(start=start, end=end, y_label=y_label, x_label=x_label, vline_pos=vline_pos, do_show=do_show,
                   legend=legend)
        return None


class LiveEvaluation:
    def __init__(self) -> None:
        self._ev_speed = EvalData('ev speed')
        self._veh_waiting = EvalData('waiting vehicles')
        self._action = EvalData('action')
        self._em_phase = EvalData('phase')
        self._em_phase_transition = EvalData('trans')
        self._ev_present = EvalData('ev present')
        return None

    def update_all(self, t: float, action: int, ev_speed: float, veh_waiting: int, em_phase: int,
                   em_phase_transition: int, ev_present: int) -> None:
        self._action.append(t, action)
        self._ev_speed.append(t, ev_speed)
        self._veh_waiting.append(t, veh_waiting)
        self._em_phase.append(t, em_phase)
        self._em_phase_transition.append(t, em_phase_transition)
        self._ev_present.append(t, ev_present)
        return None

    def get_ev_speed_data(self) -> EvalData:
        return self._ev_speed

    def get_veh_waiting_data(self) -> EvalData:
        return self._veh_waiting

    def get_action_data(self) -> EvalData:
        return self._action

    def get_em_phase_data(self) -> EvalData:
        return self._em_phase

    def get_em_phase_transition_data(self) -> EvalData:
        return self._em_phase_transition

    def get_ev_present_data(self) -> EvalData:
        return self._ev_present

    def plot_all(self, vline_pos: float = None) -> None:
        legend = []
        self._em_phase_transition.plot(do_show=False)
        legend += [self._em_phase_transition.get_ylabel()]
        self._em_phase.plot(do_show=False)
        legend += [self._em_phase.get_ylabel()]
        self._action.plot(vline_pos=vline_pos, legend=legend)
        self._ev_speed.plot(vline_pos=vline_pos)
        self._veh_waiting.plot(vline_pos=vline_pos)
        return None

    def plot_all_clipped(self, start: int = 0, end: int = None, vline_pos: float = None) -> None:
        legend = []
        self._em_phase_transition.plot_clipped(start, end, do_show=False)
        legend += [self._em_phase_transition.get_ylabel()]
        self._em_phase.plot_clipped(start, end, do_show=False)
        legend += [self._em_phase.get_ylabel()]
        self._action.plot_clipped(start, end, vline_pos=vline_pos, legend=legend)
        self._ev_speed.plot_clipped(start, end, vline_pos=vline_pos)
        self._veh_waiting.plot_clipped(start, end, vline_pos=vline_pos)
        return None
