import argparse


def get_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy',type=str,default='time',help='This is the strategy that will be used by the cache options include\n'
                                                                  '1) memory: Which will use the memory threshold for it eviction process\n'
                                                                  '2) time: It will evict the data with the least most frequent data, that passed it time threshold')
    parser.add_argument('--threshold', type=int, default='60',
                        help='This threshold is what the eviction algorithm, will use to select what data to leave the cache\n'
                             'for memory represent the argument in bytes example 300 or 2048 or 200048\n'
                             'for time represent the argument in seconds example 3600 or 216000')
    return parser.parse_args()

