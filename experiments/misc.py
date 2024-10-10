from numpy.random import default_rng, randint
from math import floor
from optparse import OptionParser
import sys


def learning_rate(remaining: float) -> float:
    max_rem = max(remaining, 0.01)
    max_dim = 5 - floor(3 * max_rem)
    dim = default_rng().integers(max_dim, 6)
    lin = max(0.1, 3 * remaining - floor(3 * remaining))
    f = 3
    for _ in range(dim):
        f *= 0.1
    return lin * f * default_rng().random()


def generate_sumo_seed() -> int:
    return 546381068 # randint(2 ** 31)


def parse_cmd():
    parser = OptionParser(usage='Usage: %s [options]' % sys.argv[0])
    parser.add_option('-s', '--seed', dest='seed', default=None, type=int)
    parser.add_option('-n', '--name', dest="name", default='ppo', type=str)
    parser.add_option('-l', '--learning-rate', dest='learning_rate', default=None, type=float)
    parser.add_option('-p', '--plot', dest='plot', default=False, action='store_true')
    parser.add_option('--evsr', '--ev-step-range', dest='ev_step_range', type=int, nargs=2, default=(1600, 1800))
    parser.add_option('--evst', '--ev-step-test', dest='ev_step_test', type=int, default=1700)
    parser.add_option('--ne', '--num-episodes', dest='num_episodes', type=int, default=1000)
    parser.add_option('--el', '--episode-length', dest='episode_length', type=int, default=180)
    parser.add_option('--tl', '--test-length', dest='test_length', type=int, default=2000)
    parser.add_option('--pls', '--pre-learn-steps', dest='pre_learn_steps', type=int, default=90)
    parser.add_option('--pds', '--post-done-steps', dest='post_done_steps', type=int, default=90)
    parser.add_option('--debug', dest='debug', default=False, action='store_true')
    parser.add_option('--sumo-output', dest='sumo_output', default=False, action='store_true')
    parser.add_option('--no-training-plot', dest='plot_training', default=True, action='store_false')
    parser.add_option('--rf', '--reward-factors', dest='reward_factors', type=float, nargs=6,
                      default=(1, 2, 3, 20, 1, 0))
    parser.add_option('--nrme', '--num-runs-mass-eval', dest='num_runs_mass_eval', type=int, default=100)
    parser.add_option('--fs', '--frame-stack-num', dest='frame_stacks', type=int, default=0)

    options, args = parser.parse_args()

    if options.learning_rate == None:
        options.learning_rate_function = learning_rate
    else:
        options.learning_rate_function = lambda _: options.learning_rate

    if options.seed != None:
        options.seed_function = lambda: options.seed
    else:
        options.seed_function = generate_sumo_seed

    options.full_name = options.name + '_seed_' + str(options.seed) + '_learningrate_' + str(
        options.learning_rate).replace('.', '_') + '_evsr_' + str(options.ev_step_range[0]) + '_' + str(
        options.ev_step_range[1])
    options.full_name += '_rew_factors'
    for f in options.reward_factors:
        options.full_name += '_' + str(int(f))

    # print('seed', options.seed, 'name', options.name, 'learning rate', options.learning_rate, 'plot', options.plot)
    # print('seed calls:', options.seed_function(), options.seed_function(), options.seed_function())
    # print('full name:', options.full_name)
    # print('learning rate calls:', options.learning_rate_function(1), options.learning_rate_function(0.5), options.learning_rate_function(0.01), options.learning_rate_function(-0.0001))
    # print('full options:', options)
    return options
