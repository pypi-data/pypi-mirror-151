import logging
from transformers import TrainerCallback

import graphsignal
from graphsignal.proto import profiles_pb2
from graphsignal.profiling_step import ProfilingStep

logger = logging.getLogger('graphsignal')

PHASE_TRAINING = 'training'

EXCLUDE_ARGS = {
    'logging_dir',
    'local_rank'
}

class GraphsignalPTCallback(TrainerCallback):
    __slots__ = [
        '_profiler',
        '_step'
    ]

    def __init__(self):
        from graphsignal.profilers.pytorch import PyTorchProfiler
        self._profiler = PyTorchProfiler()
        self._step = None

    def on_train_begin(self, args, state, control, **kwarg):
        _configure_profiler(args)

    def on_train_end(self, args, state, control, **kwarg):
        self._stop_profiler(args, state)

    def on_step_begin(self, args, state, control, **kwarg):
        self._stop_profiler(args, state)
        self._start_profiler(PHASE_TRAINING, args, state)

    def on_step_end(self, args, state, control, **kwarg):
        pass

    def _start_profiler(self, phase_name, args, state):
        if not self._step:
            self._step = ProfilingStep(
                phase_name=phase_name,
                effective_batch_size=_get_effective_batch_size(args),
                framework_profiler=self._profiler)

    def _stop_profiler(self, args, state):
        if self._step:
            if self._step._is_scheduled:
                _fill_step_stats(self._step, args, state)
            self._step.stop()
            self._step = None


class GraphsignalTFCallback(TrainerCallback):
    __slots__ = [
        '_profiler',
        '_step'
    ]

    def __init__(self):
        from graphsignal.profilers.tensorflow import TensorflowProfiler
        self._profiler = TensorflowProfiler()
        self._step = None

    def on_train_begin(self, args, state, control, **kwarg):
        _configure_profiler(args)

    def on_train_end(self, args, state, control, **kwarg):
        self._stop_profiler(args, state)

    def on_step_begin(self, args, state, control, **kwarg):
        self._stop_profiler(args, state)
        self._start_profiler(PHASE_TRAINING, args, state)

    def on_step_end(self, args, state, control, **kwarg):
        pass

    def _start_profiler(self, phase_name, args, state):
        if not self._step:
            self._step = ProfilingStep(
                phase_name=phase_name,
                effective_batch_size=_get_effective_batch_size(args),
                framework_profiler=self._profiler)

    def _stop_profiler(self, args, state):
        if self._step:
            if self._step._is_scheduled:
                _fill_step_stats(self._step, args, state)
            self._step.stop()
            self._step = None


def _get_effective_batch_size(args):
    gradient_accumulation_steps = args.gradient_accumulation_steps if args.gradient_accumulation_steps > 0 else 1
    return args.train_batch_size * args.gradient_accumulation_steps


def _fill_step_stats(step, args, state):
    step_stats = step._profile.step_stats
    if args.local_rank == -1 or args.local_rank == 0:
        step_stats.flop_count = state.total_flos
    step_stats.batch_size = args.train_batch_size
    step_stats.device_batch_size = args.per_device_train_batch_size


def _configure_profiler(args):
    if args.local_rank >= 0:
        graphsignal._agent.local_rank = args.local_rank

    if args.world_size > 0:
        graphsignal.log_parameter('world_size', args.world_size)

    for name, value in vars(args).items():
        if not name.startswith('_') and name not in EXCLUDE_ARGS and isinstance(value, (str, int, float, bool)):
            graphsignal.log_parameter(name, value)


def _log_args_prop(args, prop):
    value = getattr(args, prop, None)
    if isinstance(value, (str, int, float, bool)):
        graphsignal.log_parameter(prop, value)
